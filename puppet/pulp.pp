node 'puppetagent.local' {

file { '/mnt':
  ensure => present,
  owner => 'root',
  group => 'apache',
  mode => "2775",
}

file { '/mnt/rpms':
  ensure => directory,
}

package { 'httpd':
    ensure => 'present',
    before => File['/mnt'],
}

package { 'epel7':
    ensure => 'present',
    source => 'http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm',
    provider => 'rpm', 
}
    
wget::fetch { 'https://repos.fedorapeople.org/repos/pulp/pulp/rhel-pulp.repo':
    destination => '/etc/yum.repos.d/',
    timeout     => 15,
    verbose     => true,
}


package { [ 'qpid-cpp-server', 'qpid-cpp-server-linearstore', 'pulp-server', 'python-gofer-qpid', 'python-qpid', 'qpid-tools', 'pulp-rpm-plugins', 'pulp-puppet-plugins', 'pulp-docker-plugins', 'pulp-admin-client', 'pulp-rpm-admin-extensions', 'pulp-puppet-admin-extensions', 'pulp-docker-admin-extensions' ]:
    ensure => 'present',
}

service { [ 'httpd', 'qpidd' ]:
    ensure => 'running',
    enable    => 'true',
}

exec { 'Generating pulp certificates':
  command => 'pulp-gen-key-pair && pulp-gen-ca-certificate',
  path    => '/usr/bin',
}

class {'::mongodb::server':
  port    => 27017,
  verbose => true,
}

class {'::mongodb::client':}


mongodb_database { pulp_database:
  ensure   => present,
  tries    => 10,
  require  => Class['mongodb::server'],
}

mongodb_user { pulpadmin:
  name          => 'pulpadmin',
  ensure        => present,
  password_hash => mongodb_password('pulpadmin', 'qwedsa'),
  database      => pulp_database,
  roles         => ['readWrite', 'dbAdmin'],
  tries         => 10,
  require       => Class['mongodb::server'],
}


class { 'pulp::server':
  db_name => 'pulp_database',
  db_username => 'pulpadmin',
  db_password => 'qwedsa',
}

class { 'pulp::admin':
  pulp_server => $fqdn,
  verify_ssl => false,
}


}
