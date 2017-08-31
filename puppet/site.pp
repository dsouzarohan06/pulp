file { '/mnt':
  ensure => present,
  owner => 'root',
  group => 'apache',
  mode => "2775",
}

file { '/mnt/rpms':
  ensure => directory,
}

package { 'screen':
    ensure => 'purged',
}

#package { 'httpd':
#    ensure => 'present',
#}

#service { 'httpd':
#    ensure => 'running',
#}

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

$pkg_list = [ 'qpid-cpp-server', 'qpid-cpp-server-linearstore', 'pulp-server', 'python-gofer-qpid', 'python-qpid', 'qpid-tools', 'pulp-rpm-plugins', 'pulp-puppet-plugins', 'pulp-docker-plugins', 'pulp-admin-client', 'pulp-rpm-admin-extensions', 'pulp-puppet-admin-extensions', 'pulp-docker-admin-extensions' , 'httpd' , 'mod_ssl' ]

package { $pkg_list:
    ensure => 'present',
}

class {'::mongodb::server':
  port    => 27017,
  verbose => true,
  auth => true,
}

class {'::mongodb::client':}

#mongodb_user { myUserAdmin:
#  name          => 'myUserAdmin',
#  ensure        => present,
#  password_hash => mongodb_password('myUserAdmin', 'abc123'),
#  database      => admin,
#  roles         => ['userAdminAnyDatabase'],
#  tries         => 10,
#  require       => Class['mongodb::server'],
#}


#mongodb::db { 'pulp_database':
#  user          => 'pulpadmin',
#  password_hash => mongodb_password('pulpadmin', 'abc123'),
#}

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

#file { 'mongorc.js':
#    path          => '/root/.mongorc.js',
#    ensure        => file,
#    require       => Mongodb_user['siteUserAdmin'],
#    content       => template('my_profiles/mongo/mongorc.js.erb'),
#}

#class {'::pulp::server':}

#class { '::pulp::admin':
#  verify_ssl => false
#}

#class { '::pulp::admin':
#  verify_ssl => false
#}
