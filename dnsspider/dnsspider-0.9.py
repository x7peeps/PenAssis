#!/usr/bin/env python3
# -*- coding: latin-1 -*- ######################################################
#                ____                     _ __                                 #
#     ___  __ __/ / /__ ___ ______ ______(_) /___ __                           #
#    / _ \/ // / / (_-</ -_) __/ // / __/ / __/ // /                           #
#   /_//_/\_,_/_/_/___/\__/\__/\_,_/_/ /_/\__/\_, /                            #
#                                            /___/ team                        #
#                                                                              #
# dnsspider.py - async multithreaded subdomain bruteforcer                     #
#                                                                              #
# DESCRIPTION                                                                  #
# A very fast async multithreaded bruteforcer of subdomains that leverages a   #
# wordlist and/or character permutation.                                       #
#                                                                              #
# AUTHOR                                                                       #
# noptrix - http://www.nullsecurity.net/                                       #
#                                                                              #
# NOTES:                                                                       #
# quick'n'dirty code                                                           #
#                                                                              #
# TODO:                                                                        #
# - check if we have to scan if wildcard enabled                               #
#                                                                              #
# CHANGELOG:                                                                   #
#                                                                              #
# v0.9                                                                         #
# - use async multithreading via concurrent.futures module                     #
# - attack while mutating -> don't generate whole list when using -t 1         #
# - log only the subdomains to logfile when '-r' was chosen                    #
# - minor code clean-ups / refactoring                                         #
# - switch to tabstop=2 / shiftwidth=2                                         #
#                                                                              #
# v0.8                                                                         #
# - upgraded to python3                                                        #
#                                                                              #
# v0.7                                                                         #
# - upgraded built-in wordlist (more than 2k)                                  #
# - remove annoying timeout warnings                                           #
# - remove color output when logging to file                                   #
#                                                                              #
# v0.6                                                                         #
# - upgraded default wordlist                                                  #
# - replaced optionparser with argparse                                        #
# - add version output option                                                  #
# - fixed typo                                                                 #
#                                                                              #
# v0.5                                                                         #
# - fixed extracted ip addresses from rrset answers                            #
# - renamed file (removed version string)                                      #
# - removed trailing whitespaces                                               #
# - removed color output                                                       #
# - changed banner                                                             #
#                                                                              #
# v0.4                                                                         #
# - fixed a bug for returned list                                              #
# - added postfix option                                                       #
# - upgraded wordlist[]                                                        #
# - colorised output                                                           #
# - changed error messages                                                     #
#                                                                              #
# v0.3:                                                                        #
# - added verbose/quiet mode - default is quiet now                            #
# - fixed try/catch for domainnames                                            #
# - fixed some tab width (i normally use <= 80 chars per line)                 #
#                                                                              #
# v0.2:                                                                        #
# - append DNS and IP output to found list                                     #
# - added diffound list for subdomains resolved to different addresses         #
# - get right ip address from current used iface to avoid socket problems      #
# - fixed socket exception syntax and output                                   #
# - added usage note for fixed port and multithreaded socket exception         #
#                                                                              #
# v0.1:                                                                        #
# - initial release                                                            #
################################################################################


import sys
import time
import string
import itertools
import socket
import re
import argparse
from concurrent.futures import ThreadPoolExecutor
try:
  import dns.message
  import dns.query
except ImportError:
  print("[-] ERROR: you need the 'dnspython' package")
  sys.exit()


BANNER = '--==[ dnsspider by noptrix@nullsecurity.net ]==--'
USAGE = '\n' \
  '  dnsspider.py -t <arg> -a <arg> [options]'
VERSION = 'v0.9'

defaults = {}
hostnames = []
prefix = ''
postfix = ''
found = []
diffound = []
chars = string.ascii_lowercase
digits = string.digits

# default wordlist
wordlist = [
'0', '01', '02', '03', '1', '10', '11', '12', '13', '14', '15', '16', '17',
'18', '19', '2', '20', '3', '3com', '4', '5', '6', '7', '8', '9', 'a', 'a01',
'a02', 'a1', 'a2', 'a.auth-ns', 'abc', 'about', 'abu', 'abuja', 'ac',
'academico', 'acceso', 'access', 'accounting', 'accounts', 'accra', 'acid',
'activestat', 'ad', 'adam', 'addis', 'adkit', 'adm', 'admin', 'administracion',
'administrador', 'administrator', 'administrators', 'admins', 'ads', 'adserver',
'adsl', 'ae', 'af', 'affiliate', 'affiliates', 'afiliados', 'ag', 'agenda',
'agent', 'ai', 'ain', 'aix', 'ajax', 'ak', 'akamai', 'al', 'alabama', 'alaska',
'albuquerque', 'alerts', 'algiers', 'alpha', 'alterwind', 'am', 'amarillo',
'americas', 'amman', 'amsterdam', 'an', 'anaheim', 'analyzer', 'andorra',
'ankara', 'announce', 'announcements', 'antananarivo', 'antivirus', 'ao', 'ap',
'apache', 'api', 'apia', 'apollo', 'app', 'app01', 'app1', 'apple',
'application', 'applications', 'apps', 'appserver', 'aq', 'ar', 'arch',
'archie', 'arcsight', 'argentina', 'arizona', 'arkansas', 'arlington', 'as',
'as400', 'ashgabat', 'asia', 'asmara', 'astana', 'asterix', 'asuncion', 'at',
'athena', 'athens', 'atlanta', 'atlas', 'att', 'au', 'auction', 'austin',
'auth', 'auto', 'autodiscover', 'autorun', 'av', 'aw', 'ayuda', 'az', 'b',
'b01', 'b02', 'b1', 'b2', 'b2b', 'b2c', 'ba', 'back', 'backend', 'backtrack',
'backup', 'backups', 'baghdad', 'baker', 'bakersfield', 'baku', 'balance',
'balancer', 'baltimore', 'bamako', 'bandar', 'bangkok', 'bangui', 'banjul',
'banking', 'basseterre', 'b.auth-ns', 'bayarea', 'bb', 'bbdd', 'bbs', 'bd',
'bdc', 'be', 'bea', 'beijing', 'beirut', 'belfast', 'belgrade', 'belmopan',
'berlin', 'bern', 'beta', 'bf', 'bg', 'bh', 'bi', 'bill', 'billing', 'bishkek',
'bissau', 'biz', 'biztalk', 'bj', 'black', 'blackberry', 'blackboard', 'blog',
'blogs', 'blue', 'bm', 'bn', 'bnc', 'bo', 'board', 'bob', 'bof', 'bogota',
'boise', 'bolsa', 'border', 'boston', 'boulder', 'boy', 'br', 'brasilia',
'bratislava', 'bravo', 'brazil', 'brazzaville', 'bridgetown', 'britian',
'broadcast', 'broker', 'bronze', 'brown', 'brussels', 'bs', 'bsc', 'bsd',
'bsd0', 'bsd01', 'bsd02', 'bsd1', 'bsd2', 'bsdi', 'bss', 'bt', 'bts',
'bucharest', 'budapest', 'buenos', 'bug', 'buggalo', 'bugs', 'bugzilla',
'build', 'bujumbura', 'bulletins', 'burn', 'burner', 'buscador', 'buy', 'bv',
'bw', 'by', 'bz', 'c', 'ca', 'cache', 'cafe', 'cairo', 'calendar', 'california',
'call', 'calvin', 'canada', 'canal', 'canberra', 'canon', 'caracas', 'cardiff',
'careers', 'cart', 'castries', 'catalog', 'catalogue', 'c.auth-ns', 'cayenne',
'cc', 'cd', 'cdburner', 'cdn', 'centos', 'central', 'cert', 'certificates',
'certify', 'certserv', 'certsrv', 'cf', 'cg', 'cgi', 'ch', 'channel',
'channels', 'charlie', 'charlotte', 'chat', 'chats', 'chatserver', 'check',
'checkpoint', 'chi', 'chicago', 'chimera', 'chisinau', 'chronos', 'ci', 'cims',
'cincinnati', 'cisco', 'citrix', 'ck', 'cl', 'class', 'classes', 'classifieds',
'classroom', 'cleveland', 'cli', 'clicktrack', 'client', 'clientes', 'clients',
'clix', 'club', 'clubs', 'cluster', 'clusters', 'cm', 'cmail', 'cms', 'cn',
'co', 'cocoa', 'code', 'coldfusion', 'colombo', 'colombus', 'colorado',
'columbus', 'com', 'commerce', 'commerceserver', 'communigate', 'community',
'compaq', 'compras', 'con', 'conakry', 'concentrator', 'conf', 'conference',
'conferencing', 'confidential', 'connect', 'connecticut', 'consola', 'console',
'consult', 'consultant', 'consultants', 'consulting', 'consumer', 'contact',
'content', 'contracts', 'control', 'controller', 'copenhagen', 'core', 'core0',
'core01', 'corp', 'corpmail', 'corporate', 'correo', 'correoweb', 'cortafuegos',
'counterstrike', 'courses', 'cpanel', 'cr', 'cricket', 'crm', 'crs', 'cs',
'cso', 'css', 'ct', 'cu', 'cust1', 'cust10', 'cust100', 'cust101', 'cust102',
'customer', 'customers', 'cv', 'cvs', 'cx', 'cy', 'cz', 'd', 'dakar', 'dallas',
'damascus', 'dar', 'darwin', 'data', 'database', 'database01', 'database02',
'database1', 'database2', 'databases', 'datastore', 'datos', 'david', 'db',
'db0', 'db01', 'db02', 'db1', 'db2', 'dc', 'de', 'dealers', 'debian', 'dec',
'def', 'default', 'defiant', 'delaware', 'dell', 'delta', 'delta1', 'demo',
'demon', 'demonstration', 'demos', 'denver', 'depot', 'des', 'desarrollo',
'descargas', 'design', 'designer', 'desktop', 'detroit', 'dev', 'dev0', 'dev01',
'dev1', 'devel', 'develop', 'developer', 'developers', 'development', 'device',
'devserver', 'devsql', 'dhaka', 'dhcp', 'dial', 'dialer', 'dialup', 'diana',
'digital', 'dilbert', 'dili', 'dir', 'direct', 'directory', 'disc', 'discovery',
'discuss', 'discussion', 'discussions', 'disk', 'disney', 'distributer',
'distributers', 'dj', 'djibouti', 'dk', 'dm', 'dmail', 'dmz', 'dnews', 'dns',
'dns0', 'dns1', 'dns2', 'dns-2', 'dns3', 'do', 'doc', 'docs', 'document',
'documentacion', 'documentos', 'doha', 'domain', 'domaincontroller',
'domain-controller', 'domains', 'dominio', 'domino', 'dominoweb', 'doom',
'download', 'downloads', 'downtown', 'dragon', 'dragonflybsd', 'drupal',
'dsl', 'dublin', 'dushanbe', 'dyn', 'dynamic', 'dynip', 'dz', 'e', 'e0',
'eaccess', 'eagle', 'earth', 'east', 'ec', 'echo', 'ecom', 'e-com', 'ecommerce',
'e-commerce', 'edi', 'edinburgh', 'edu', 'education', 'edward', 'ee', 'eg',
'eh', 'ejemplo', 'elpaso', 'email', 'employees', 'empresa', 'empresas', 'en',
'enable', 'eng', 'eng01', 'eng1', 'engine', 'engineer', 'engineering',
'enrutador', 'enterprise', 'epsilon', 'er', 'erp', 'es', 'esd', 'esm',
'espanol', 'estadisticas', 'esx', 'et', 'eta', 'europe', 'events', 'ex',
'example', 'examples', 'exchange', 'exec', 'exim', 'exit', 'ext', 'extern',
'external', 'extranet', 'f', 'f5', 'falcon', 'farm', 'faststats', 'fax',
'fedora', 'fedoracore', 'feedback', 'feeds', 'fi', 'field', 'file', 'files',
'fileserv', 'fileserver', 'filestore', 'filter', 'finance', 'find', 'finger',
'firewall', 'fix', 'fixes', 'fj', 'fk', 'fl', 'flash', 'florida', 'flow', 'fm',
'fo', 'foobar', 'formacion', 'foro', 'foros', 'fortworth', 'forum', 'forums',
'foto', 'fotos', 'foundry', 'fox', 'foxtrot', 'fr', 'france', 'frank', 'fred',
'freebsd', 'freebsd0', 'freebsd01', 'freebsd02', 'freebsd1', 'freebsd2',
'freetown', 'freeware', 'fresno', 'front', 'frontdesk', 'fs', 'fsp', 'ftp',
'ftp-', 'ftp0', 'ftp2', 'ftpd', 'ftpserver', 'fw', 'fw1', 'fw-1', 'fwsm',
'fwsm0', 'fwsm01', 'fwsm1', 'g', 'ga', 'gaborone', 'galeria', 'galerias',
'galleries', 'gallery', 'games', 'gamma', 'gandalf', 'gate', 'gatekeeper',
'gateway', 'gauss', 'gd', 'ge', 'gemini', 'general', 'gentoo', 'george',
'georgetown', 'georgia', 'germany', 'gf', 'gg', 'gh', 'gi', 'gilford', 'git',
'gl', 'glendale', 'gm', 'gmail', 'gn', 'go', 'gold', 'goldmine', 'golf',
'gopher', 'gp', 'gprs', 'gq', 'gr', 'green', 'group', 'groups', 'groupwise',
'gs', 'gsx', 'gt', 'gu', 'guatemala', 'guest', 'guide', 'gw', 'gw1', 'gy', 'h',
'hal', 'halflife', 'hanoi', 'harare', 'havana', 'hawaii', 'hello', 'help',
'helpdesk', 'helponline', 'helsinki', 'henry', 'hera', 'heracles', 'hercules',
'hermes', 'hi', 'hidden', 'hk', 'hm', 'hn', 'hobbes', 'hollywood', 'home',
'homebase', 'homer', 'honeypot', 'honiara', 'honolulu', 'host', 'host1',
'host3', 'host4', 'host5', 'hotel', 'hotjobs', 'hotspot', 'houstin', 'houston',
'howto', 'hp', 'hpc', 'hpov', 'hpux', 'hp-ux', 'hr', 'ht', 'http', 'https',
'hu', 'hub', 'humanresources', 'hypernova', 'i', 'ia', 'ias', 'ibm', 'ibmdb',
'id', 'ida', 'idaho', 'ids', 'ie', 'iis', 'il', 'illinois', 'ILMI', 'im',
'image', 'images', 'imail', 'imap', 'imap3', 'imap3d', 'imap4', 'imapd',
'imaps', 'img', 'img0', 'img01', 'img02', 'imgs', 'in', 'inbound', 'inc',
'include', 'incoming', 'india', 'indiana', 'indianapolis', 'info', 'informix',
'inside', 'install', 'int', 'interface', 'intern', 'internal', 'international',
'internet', 'intl', 'intranet', 'invalid', 'investor', 'investors', 'io',
'iota', 'iowa', 'ip', 'ip6', 'iplanet', 'ipmonitor', 'ipsec', 'ipsec-gw',
'ipsp', 'ipv6', 'iq', 'ir', 'irc', 'ircd', 'ircserver', 'ireland', 'iris',
'irix', 'irvine', 'irving', 'is', 'isa', 'isaserv', 'isaserver',
'islamabad', 'ism', 'israel', 'isync', 'it', 'italy', 'ix', 'j', 'jabber',
'jakarta', 'japan', 'java', 'jboss', 'je', 'jedi', 'jm', 'jo', 'jobs', 'john',
'jp', 'jrun', 'juba', 'juegos', 'juliet', 'juliette', 'juniper', 'jupiter', 'k',
'kabul', 'kampala', 'kansas', 'kansascity', 'kappa', 'kathmandu', 'kb', 'ke',
'kentucky', 'kerberos', 'keynote', 'kg', 'kh', 'khartoum', 'ki', 'kiev',
'kigali', 'kilo', 'king', 'kingston', 'kingstown', 'kinshasa', 'km', 'kn',
'knowledgebase', 'knoxville', 'koe', 'korea', 'kp', 'kr', 'ks', 'kuala',
'kuwait', 'kw', 'ky', 'kz', 'l', 'la', 'lab', 'laboratories', 'laboratory',
'labs', 'lambda', 'lan', 'laptop', 'laserjet', 'lasvegas', 'launch', 'lb', 'lc',
'ldap', 'legal', 'leo', 'li', 'lib', 'library', 'libreville', 'lilongwe',
'lima', 'lincoln', 'link', 'linux', 'linux0', 'linux01', 'linux02', 'linux1',
'linux2', 'lisa', 'lisbon', 'lista', 'lists', 'listserv', 'listserver', 'live',
'ljubljana', 'lk', 'load', 'loadbalancer', 'local', 'localhost', 'log', 'log0',
'log01', 'log02', 'log1', 'log2', 'logfile', 'logfiles', 'logger', 'logging',
'loghost', 'login', 'logon', 'logs', 'lome', 'london', 'longbeach',
'losangeles', 'lotus', 'louisiana', 'lr', 'ls', 'lt', 'lu', 'luanda', 'luke',
'lusaka', 'luxembourg', 'lv', 'ly', 'lyris', 'm', 'ma', 'mac', 'mac1', 'mac10',
'mac11', 'mac2', 'mac3', 'mac4', 'mac5', 'mach', 'macintosh', 'madrid', 'mail',
'mail2', 'mailer', 'mailgate', 'mailhost', 'mailing', 'maillist', 'maillists',
'mailroom', 'mailserv', 'mailsite', 'mailsrv', 'main', 'maine', 'maint',
'majuro', 'malabo', 'male', 'mall', 'manage', 'management', 'manager',
'managers', 'managua', 'manama', 'mandrake', 'mandriva', 'manila',
'manufacturing', 'map', 'mapas', 'maps', 'maputo', 'marketing', 'marketplace',
'mars', 'marvin', 'mary', 'maryland', 'maseru', 'massachusetts', 'master',
'max', 'mbabana', 'mc', 'mci', 'md', 'mdaemon', 'me', 'media', 'melekeok',
'member', 's', 'master', 'max', 'mbabana', 'mc', 'mci', 'md', 'mdaemon', 'me',
'media', 'melekeok', 'member', 'members', 'memphis', 'mercury', 'merlin',
'messages', 'messenger', 'meta', 'mexico', 'mg', 'mgc', 'mgmt', 'mh', 'mi',
'miami', 'michigan', 'mickey', 'midwest', 'mike', 'milwaukee', 'minerva',
'minneapolis', 'minnesota', 'minsk', 'mint', 'mirror', 'mis', 'mississippi',
'missouri', 'mk', 'ml', 'mm', 'mn', 'mngt', 'mo', 'mob', 'mobile', 'mogadishu',
'mom', 'monaco', 'monitor', 'monitoring', 'monrovia', 'montana', 'montevideo',
'moodle', 'moon', 'moroni', 'moscow', 'movies', 'mozart', 'mp', 'mp3', 'mpeg',
'mpg', 'mq', 'mr', 'mrtg', 'ms', 'msexchange', 'ms-exchange', 'mssql', 'ms-sql',
'mssql0', 'mssql01', 'mssql1', 'mt', 'mta', 'mtu', 'mu', 'multimedia', 'muscat',
'music', 'mv', 'mw', 'mx', 'mx01', 'my', 'mysql', 'mysql0', 'mysql01', 'mysql1',
'mz', 'n', 'na', 'nairobi', 'name', 'names', 'nameserv', 'nameserver', 'nas',
'nashville', 'nassau', 'nat', 'nc', 'nd', 'ndjamena', 'nds', 'ne', 'nebraska',
'nelson', 'neon', 'neptune', 'net', 'netapp', 'netbsd', 'netdata', 'netgear',
'netmail', 'netmeeting', 'netscaler', 'netscreen', 'netstats', 'netware',
'network', 'nevada', 'new', 'newhampshire', 'newjersey', 'newmexico',
'neworleans', 'news', 'newsfeed', 'newsfeeds', 'newsgroups', 'newton',
'newyork', 'newzealand', 'nf', 'ng', 'nh', 'ni', 'niamey', 'nicosia', 'nigeria',
'nj', 'nl', 'nm', 'nms', 'nntp', 'no', 'noc', 'node', 'nokia', 'nombres',
'nora', 'north', 'northcarolina', 'northdakota', 'northeast', 'northwest',
'noticias', 'nouakchott', 'novell', 'november', 'np', 'nr', 'ns', 'ns-', 'ns0',
'ns01', 'ns02', 'ns1', 'ns2', 'ns3', 'ns4', 'ns5', 'nt', 'nt4', 'nt40',
'ntmail', 'ntp', 'ntpd', 'ntserver', 'nu', 'nukualofa', 'null', 'nv', 'ny',
'nz', 'o', 'oakland', 'ocean', 'odin', 'office', 'offices', 'oh', 'ohio', 'ok',
'oklahoma', 'oklahomacity', 'old', 'om', 'omaha', 'omega', 'omicron', 'online',
'ontario', 'op', 'open', 'openbsc', 'openbsd', 'openbts', 'openserver',
'opensolaris', 'opensuse', 'openview', 'openvms', 'operations', 'ops', 'ops0',
'ops01', 'ops02', 'ops1', 'ops2', 'opsware', 'or', 'oracle', 'orange', 'order',
'orders', 'oregon', 'orion', 'orlando', 'os', 'os390', 'oscar', 'oslo', 'osx',
'ottawa', 'ouagadougou', 'out', 'outbound', 'outdial', 'outgoing', 'outlook',
'outside', 'ov', 'owa', 'owa01', 'owa02', 'owa1', 'owa2', 'ows', 'oxnard', 'p',
'pa', 'pad', 'page', 'pager', 'pages', 'paginas', 'palikir', 'panama', 'papa',
'paramaribo', 'paris', 'parners', 'partner', 'partners', 'patch', 'patches',
'paul', 'payroll', 'pbx', 'pc', 'pc01', 'pc1', 'pc10', 'pc101', 'pc11', 'pc12',
'pc13', 'pc14', 'pc15', 'pc16', 'pc17', 'pc18', 'pc19', 'pc2', 'pc20',
'pcanywhere', 'pcbsd', 'pcmail', 'pcu', 'pda', 'pdc', 'pe', 'pegasus',
'pendrell', 'pennsylvania', 'peoplesoft', 'personal', 'pf', 'pg', 'pgp', 'ph',
'phi', 'philadelphia', 'phnom', 'phoenix', 'phoeniz', 'phone', 'phones',
'photo', 'photos', 'phpmyadmin', 'pi', 'pics', 'pictures', 'pink', 'pipex-gw',
'pittsburgh', 'pix', 'pk', 'pki', 'pl', 'plano', 'platinum', 'plesk', 'pluto',
'pm', 'pm1', 'pma', 'pn', 'po', 'podgorica', 'policy', 'polls', 'pop', 'pop3',
'port', 'portal', 'portals', 'portfolio', 'portland', 'porto', 'post',
'postales', 'postgresql', 'postman', 'postmaster', 'postoffice', 'pp', 'ppp',
'ppp1', 'ppp10', 'ppp11', 'ppp12', 'ppp13', 'ppp14', 'ppp15', 'ppp16', 'ppp17',
'ppp18', 'ppp19', 'ppp2', 'ppp20', 'ppp21', 'ppp3', 'ppp4', 'ppp5', 'ppp6',
'ppp7', 'ppp8', 'ppp9', 'pptp', 'pr', 'prague', 'praia', 'pre', 'prensa',
'preprod', 'pre-prod', 'press', 'pretoria', 'printer', 'printserv',
'printserver', 'pristina', 'priv', 'privacy', 'private', 'problemtracker',
'prod', 'products', 'profiles', 'project', 'projects', 'promo', 'proxy',
'prueba', 'pruebas', 'ps', 'psi', 'pss', 'pt', 'pub', 'public', 'pubs',
'purple', 'pw', 'py', 'pyongyang', 'q', 'qa', 'qmail', 'qnx', 'qotd', 'quake',
'quebec', 'queen', 'quito', 'quotes', 'r', 'r01', 'r02', 'r1', 'r2', 'ra',
'rabat', 'rack', 'radio', 'radius', 'rangoon', 'rapidsite', 'raptor', 'ras',
'rc', 'rcs', 'rd', 're', 'read', 'realserver', 'recruiting', 'red', 'redhat',
'ref', 'reference', 'reg', 'register', 'registro', 'registry', 'regs', 'relay',
'release', 'rem', 'remote', 'remstats', 'report', 'reports', 'research',
'reseller', 'reserved', 'restricted', 'resumenes', 'reykjavik', 'rhel', 'rho',
'rhodeisland', 'ri', 'riga', 'ris', 'risc', 'riyadh', 'rmi', 'ro', 'robert',
'robinhood', 'rome', 'romeo', 'root', 'rose', 'roseau', 'route', 'router',
'router1', 'rs', 'rss', 'rtelnet', 'rtr', 'rtr01', 'rtr1', 'ru', 'rune', 'rw',
'rwhois', 's', 's1', 's2', 'sa', 'sabayon', 'sac', 'sacramento', 'sadmin',
'safe', 'saint', 'sales', 'saltlake', 'sam', 'sample', 'san', 'sanaa',
'sanantonio', 'sandbox', 'sandiego', 'sanfrancisco', 'sanjose', 'santiago',
'santo', 'sao', 'sarajevo', 'saskatchewan', 'saturn', 'sb', 'sbs', 'sc',
'scanner', 'schedules', 'sco', 'scotland', 'scotty', 'scp', 'sd', 'se',
'search', 'seattle', 'sec', 'secret', 'secure', 'secured', 'securid',
'security', 'sendmail', 'seoul', 'seri', 'serv', 'serv2', 'server', 'server1',
'servers', 'service', 'services', 'servicio', 'servidor', 'setup', 'sg', 'sgsn',
'sh', 'share', 'shared', 'sharepoint', 'shares', 'shareware', 'shipping',
'shop', 'shoppers', 'shopping', 'si', 'siebel', 'sierra', 'sigma', 'signin',
'signup', 'silver', 'sim', 'singapore', 'sip', 'sirius', 'site', 'sj', 'sk',
'skopje', 'skywalker', 'sl', 'slack', 'slackware', 'slmail', 'sm', 'smc', 'sms',
'smsc', 'smtp', 'smtphost', 'sn', 'sniffer', 'snmp', 'snmpd', 'snoopy', 'snort',
'so', 'socal', 'sofia', 'software', 'sol', 'solaris', 'solutions', 'soporte',
'source', 'sourcecode', 'sourcesafe', 'south', 'southcarolina', 'southdakota',
'southeast', 'southwest', 'spain', 'spam', 'spider', 'spiderman', 'splunk',
'spock', 'spokane', 'springfield', 'sprint', 'sqa', 'sql', 'sql0', 'sql01',
'sql1', 'sql7', 'sqlserver', 'squid', 'squirrel', 'squirrelmail', 'sr', 'srv',
'ss', 'ss7', 'ssh', 'ssl', 'ssl0', 'ssl01', 'ssl1', 'ssp', 'st', 'staff',
'stage', 'stage1', 'staging', 'start', 'stat', 'static', 'statistics', 'stats',
'stlouis', 'stock', 'stockholm', 'storage', 'store', 'storefront', 'stp',
'streaming', 'stronghold', 'strongmail', 'studio', 'submit', 'subversion',
'sun', 'sun0', 'sun01', 'sun02', 'sun1', 'sun2', 'superman', 'supplier',
'suppliers', 'support', 'suse', 'suva', 'sv', 'svn', 'sw', 'sw0', 'sw01', 'sw1',
'sweden', 'switch', 'switzerland', 'sy', 'sybase', 'sydney', 'sysadmin',
'sysback', 'syslog', 'syslogs', 'system', 'sz', 't', 'tacas', 'tacoma',
'taipei', 'taiwan', 'talk', 'tallinn', 'tampa', 'tango', 'tarawa', 'tashkent',
'tau', 'tbilisi', 'tc', 'tcl', 'td', 'team', 'tech', 'technology',
'techsupport', 'tegucigalpa', 'tehran', 'tel', 'telephone', 'telephony',
'telnet', 'temp', 'tennessee', 'terminal', 'terminalserver', 'termserv', 'test',
'test2k', 'testbed', 'testing', 'testlab', 'testlinux', 'tests', 'testserver',
'testsite', 'testsql', 'testxp', 'texas', 'tf', 'tftp', 'tg', 'th', 'thailand',
'theta', 'thimphu', 'thor', 'tienda', 'tiger', 'time', 'tirana', 'titan',
'tivoli', 'tj', 'tk', 'tm', 'tn', 'to', 'tokyo', 'toledo', 'tom', 'tool',
'tools', 'toplayer', 'toronto', 'tour', 'tp', 'tr', 'tracker', 'train',
'training', 'transfers', 'trinidad', 'trinity', 'tripoli', 'ts', 'ts1', 'tt',
'tucson', 'tulsa', 'tunis', 'tunnel', 'tv', 'tw', 'tx', 'tz', 'u', 'ua',
'ubuntu', 'uddi', 'ug', 'uk', 'ulaanbaatar', 'um', 'un', 'uniform', 'union',
'unitedkingdom', 'unitedstates', 'unix', 'unixware', 'update', 'updates',
'upload', 'uploads', 'ups', 'upsilon', 'uranus', 'urchin', 'us', 'usa',
'usenet', 'user', 'users', 'ut', 'utah', 'utilities', 'uy', 'uz', 'v', 'va',
'vader', 'vaduz', 'vaiaku', 'valletta', 'vantive', 'vatican', 'vault', 'vc',
've', 'vega', 'vegas', 'vend', 'vendors', 'venus', 'vermont', 'vg', 'vi',
'victor', 'victoria', 'video', 'videos', 'vienna', 'vientiane', 'viking',
'vilnius', 'violet', 'vip', 'virginia', 'virtual', 'vista', 'vm', 'vms',
'vmserver', 'vmware', 'vn', 'vnc', 'voice', 'voicemail', 'voip', 'voyager',
'vpn', 'vpn0', 'vpn01', 'vpn02', 'vpn1', 'vpn2', 'vt', 'vu', 'vz', 'w', 'w1',
'w2', 'w3', 'wa', 'wais', 'wallet', 'wam', 'wan', 'wap', 'warehouse', 'warsaw',
'washington', 'wc3', 'web', 'webaccess', 'webadmin', 'webalizer', 'webboard',
'webcache', 'webcam', 'webcast', 'webct', 'webdev', 'webdocs', 'webfarm',
'webhelp', 'weblib', 'weblog', 'weblogic', 'webmail', 'webmaster', 'webmin',
'webproxy', 'webring', 'webs', 'webserv', 'webserver', 'webservices', 'webshop',
'website', 'websites', 'websphere', 'websrv', 'websrvr', 'webstats', 'webstore',
'websvr', 'webtrends', 'welcome', 'wellington', 'west', 'westvirginia', 'wf',
'whiskey', 'white', 'whois', 'wi', 'wichita', 'wiki', 'wililiam', 'win',
'win01', 'win02', 'win1', 'win2', 'win2000', 'win2003', 'win2k', 'win2k3',
'windhoek', 'windows', 'windows01', 'windows02', 'windows1', 'windows2',
'windows2000', 'windows2003', 'windowsxp', 'wingate', 'winnt', 'winproxy',
'wins', 'winserve', 'winxp', 'wire', 'wireless', 'wisconsin', 'wlan',
'wordpress', 'work', 'workstation', 'world', 'wpad', 'write', 'ws', 'ws1',
'ws10', 'ws11', 'ws12', 'ws13', 'ws2', 'ws3', 'ws4', 'ws5', 'ws6', 'ws7', 'ws8',
'ws9', 'wusage', 'wv', 'ww', 'www', 'www-', 'www0', 'www01', 'www-01', 'www02',
'www-02', 'www1', 'www-1', 'www2', 'www-2', 'www3', 'wwwchat', 'wwwdev',
'www-int', 'wwwmail', 'wy', 'wyoming', 'x', 'x25', 'x25gw', 'x25pad', 'xanthus',
'xi', 'xlogan', 'xmail', 'xml', 'xot', 'xp', 'x-ray', 'y', 'yamoussoukro',
'yankee', 'yaounde', 'ye', 'yellow', 'yerevan', 'young', 'yt', 'yu', 'z', 'za',
'zagreb', 'zebra', 'zenwalk', 'zera', 'zeus', 'zlog', 'z-log', 'zm', 'zos',
'zulu', 'zvm', 'zvse', 'zw'
]


def usage():
  print('\n' + USAGE)
  sys.exit()

  return


def check_usage():
  if len(sys.argv) == 1:
    print('[!] WARNING: use -H for help and usage')
    sys.exit()

  return


def get_default_nameserver():
  print('[+] getting default nameserver')
  lines = list(open('/etc/resolv.conf', 'r'))
  for line in lines:
    line = line.strip()
    if not line or line[0] == ';' or line[0] == '#':
      continue
    fields = line.split()
    if len(fields) < 2:
      continue
    if fields[0] == 'nameserver':
      defaults['nameserver'] = fields[1]
      return defaults

  return


def get_default_source_ip():
  print('[+] getting default ip address')
  try:
    # get current used iface enstablishing temp socket
    ipsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipsocket.connect(("gmail.com", 80))
    defaults['ipaddr'] = ipsocket.getsockname()[0]
    print('[+] found currently used interface ip ' + "'" + defaults['ipaddr'] \
      + "'")
    ipsocket.close()
  except:
    print(''' [!] WARNING: can\'t get your ip-address, use "-i" option and
      define yourself''')

  return defaults


def parse_cmdline():
  p = argparse.ArgumentParser(usage=USAGE, add_help=False)
  p.add_argument(
    '-t', metavar='<type>', dest='type',
    help='attack type (0 for dictionary 1 for bruteforce)'
  )
  p.add_argument(
    '-a', metavar='<domain>', dest='domain', help='subdomain to bruteforce'
  )
  p.add_argument(
    '-l', metavar='<wordlist>', dest='wordlist',
    help='wordlist, one hostname per line (default: built-in)'
  )
  p.add_argument(
    '-d', metavar='<nameserver>', dest='dnshost',
    help="choose another nameserver (default: your system's)"
  )
  p.add_argument(
    '-i', metavar='<ipaddr>', dest='ipaddr',
    help="source ip address to use (default: your system's)"
  )
  p.add_argument(
    '-p', metavar='<port>', dest='port', type=int, default=0,
    help='source port to use (default: 0 -> first free random port)'
  )
  p.add_argument(
    '-u', metavar='<protocol>', dest='protocol', default='udp',
    help='speak via udp or tcp (default: udp)'
  )
  p.add_argument(
    '-c', metavar='<charset>', dest='charset', default=0,
    help='choose charset 0 [a-z0-9], 1 [a-z] or 2 [0-9] (default: 0)'
  )
  p.add_argument(
    '-m', metavar='<maxchar>', dest='max', type=int, default=2,
    help='max chars to bruteforce (default: 2)'
  )
  p.add_argument(
    '-s', metavar='<prefix>', dest='prefix',
    help="prefix for bruteforce, e.g. 'www'"
  )
  p.add_argument(
    '-g', metavar='<postfix>', dest='postfix',
    help="postfix for bruteforce, e.g. 'www'"
  )
  p.add_argument(
    '-o', metavar='<sec>', dest='timeout', default=3,
    help='timeout (default: 3)'
  )
  p.add_argument(
    '-v', action='store_true', dest='verbose',
    help='verbose mode - prints every attempt (default: quiet)'
  )
  p.add_argument(
    '-w', metavar='<sec>', dest='wait', default=0,
    help='seconds to wait for next request (default: 0)'
  )
  p.add_argument(
    '-x', metavar='<num>', dest='threads', type=int, default=32,
    help='number of threads to use (default: 32) - choose more :)'
  )
  p.add_argument(
    '-r', metavar='<logfile>', dest='logfile', default='stdout',
    help='write found subdomains to file (default: stdout)'
  )
  p.add_argument(
    '-V', action='version', version='%(prog)s ' + VERSION,
    help='print version information'
  )
  p.add_argument('-H', action='help', help='print this help')

  return(p.parse_args())


def check_cmdline(opts):
  if not opts.type or not opts.domain:
    print('[-] ERROR: mount /dev/brain')
    sys.exit()

  return


def set_opts(defaults, opts):
  if not opts.dnshost:
    opts.dnshost = defaults['nameserver']
  if not opts.ipaddr:
    opts.ipaddr = defaults['ipaddr']
  if int(opts.charset) == 0:
    opts.charset = chars + digits
  elif int(opts.charset) == 1:
    opts.charset = chars
  else:
    opts.charset = digits
  if not opts.prefix:
    opts.prefix = prefix
  if not opts.postfix:
    opts.postfix = postfix

  return opts


def read_hostnames(opts):
  print('[+] reading hostnames')
  hostnames = []
  if opts.wordlist:
    hostnames = list(open(opts.wordlist, 'r'))
    return hostnames
  else:
    return wordlist

  return


def attack(opts, hostname):
  if opts.verbose:
    sys.stdout.write('    > trying %s\n' % hostname)
    sys.stdout.flush()
  try:
    x = dns.message.make_query(hostname, 1)
    if opts.protocol == 'udp':
      a = dns.query.udp(x, opts.dnshost, float(opts.timeout), 53, None,
        opts.ipaddr, opts.port, True, False)
    else:
      a = dns.query.tcp(x, opts.dnshost, float(opts.timeout), 53, None,
        opts.ipaddr, opts.port, False)
  except dns.exception.Timeout:
    sys.exit()
  except socket.error:
    print('''[-] ERROR: no connection? ip|srcport incorrectly defined? you can
           run only one thread if fixed source port specified!''')
    sys.exit()
  if a.answer:
    answ = ''
    # iterate dns rrset answer (can be multiple sets) field to extract
    # detailed info (dns and ip)
    for i in a.answer:
      answ += str(i[0])
      answ += ' '
    answer = (hostname, answ)
    found.append(answer)
  else:
    pass

  return


def prepare_attack(opts, hostnames):
  _hostnames = []
  sys.stdout.write('[+] attacking \'%s\' via ' % opts.domain)
  if opts.type == '0':
    sys.stdout.write('dictionary\n')
    for hostname in hostnames:
      _hostnames.append(hostname.rstrip() + '.' + opts.domain)
  elif opts.type == '1':
    sys.stdout.write('bruteforce\n')
    for hostname in itertools.product(opts.charset, repeat=opts.max):
      _hostnames.append(opts.prefix + ''.join(hostname) + opts.postfix + '.' + \
        opts.domain)
  else:
    print('[-] ERROR: unknown attack type')
    sys.exit()

  with ThreadPoolExecutor(opts.threads) as exe:
    for hostname in _hostnames:
      time.sleep(float(opts.wait))
      exe.submit(attack, opts, hostname)

  return


def ip_extractor(ip):
  # extract ip from string of rrset answer object
  try:
    extracted = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip)
    return extracted[0]
  except:
    print('[-] ERROR: can\'t extract ip addresses')
    sys.exit()

  return


def analyze_results(opts, found):
  # get maindomain ip
  try:
    mainhostip = socket.gethostbyname(opts.domain)
    # append domain|ip to diffound if subdomain ip different than starting
    # domain ip
    ([diffound.append(domain + ' | ' + ip) \
      for domain, ip in found if ip_extractor(ip) != mainhostip])
  except dns.exception.Timeout:
    sys.exit()
  except socket.error:
    print('[-] ERROR: wrong domain or no connection?')
    sys.exit()

  return


def log_results(opts, found, diffound):
  if opts.logfile == 'stdout':
    print('---')
    if not found:
      print('no hosts found :(')
    else:
      print('ANSWERED DNS REQUESTS')
      print('---')
      for f in found:
        print(f[0] + ' | ' + f[1])
    if not diffound:
      print('---')
      print('NO HOSTS WITH DIFFERENT IP FOUND :(')
    else:
      print('---')
      print('ANSWERED DNS REQUEST WITH DIFFERENT IP')
      print('---')
      for domain in diffound:
        print(domain)
  else:
    print('[+] logging results to %s' % opts.logfile)
    with open(opts.logfile, 'w') as f:
      if found:
        for x in found:
          f.write(x[0] + '\n')
      if diffound:
        for domain in diffound:
          f.write(domain + '\n')
  print('[+] game over')

  return


def main():
  check_usage()
  opts = parse_cmdline()
  check_cmdline(opts)
  if not opts.dnshost:
    defaults = get_default_nameserver()
  if not opts.ipaddr:
    defaults = get_default_source_ip()
  if opts.protocol != 'udp' and opts.protocol != 'tcp':
    print('[-] ERROR: unknown protocol')
    sys.exit(1337)
  opts = set_opts(defaults, opts)
  hostnames = read_hostnames(opts)
  prepare_attack(opts, hostnames)
  #analyze_results(opts, found)
  log_results(opts, found, diffound)

  return


if __name__ == '__main__':
  try:
    print(BANNER + '\n')
    main()
  except KeyboardInterrupt:
    print('\n[!] WARNING: aborted by user')
    raise SystemExit


# EOF

