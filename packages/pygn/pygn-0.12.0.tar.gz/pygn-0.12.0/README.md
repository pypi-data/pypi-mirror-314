Python Gateway Script from news to mail and vice versa.

Copyright:\
Copyright (C) 2000-2001,2012 Cosimo Alfarano <kalfa@debian.org>\
Copyright (C) 2014 Matěj Cepl <mcepl@cepl.eu>

A copy of the GNU General Public License, version 3, can be found in
the file COPYING.

It is intended to be a full SMTP/NNTP rfc compliant gateway
with whitelist manager.

You will probably have to install a mail-transport-agent and/or
news-transport-system package to manage SMTP/NNTP traffic.

MTA is needed for mail2news service, since mail have to be
processed on a box where pyg is installed. You can use a remote
smtpserver for news2mail.

News system is useful but not needed, since you can send articles to a
remote SMTP server (ie: moderated NG) where is installed pyg, otherwise you
will need it.

It refers to rfc 822 (mail) and 850 (news).

----------------

All issues, questions, complaints, or (even better!) patches
should be send via email to
[~mcepl/devel@lists.sr.ht](mailto:~mcepl/devel@lists.sr.ht) email
list (for patches use [git
send-email](https://git-send-email.io/)).

