"""News to mail gateway script. Copyright 2000 Cosimo Alfarano

Author: Cosimo Alfarano
Date: June 11 2000

news2mail.py - (C) 2000 by Cosimo Alfarano <Alfarano@Students.CS.UniBo.It>
You can use this software under the terms of the GPL. If we meet some day,
and you think this stuff is worth it, you can buy me a beer in return.

Thanks to md for this useful formula. Beer is beer.

Gets news article and sends it via SMTP.

class news2mail is hopefully conform to rfc822.

normal (what pygs does) operations flow is:
1) reads from stdin NNTP article (readfile)
2) divide headers and body (parsearticle)
3) merges NNTP and SMTP heads into a unique heads
4) adds, renames and removes some heads
5) sorts remaining headers starting at top with Received: From: To: Subject:
    Date:, normal headers ending with X-* and Resent-* headers.

"""
import argparse
from collections import OrderedDict
import email
import email.policy
import os
import smtplib
from socket import gethostbyaddr, gethostname
import sys
import time
import whitelist
import mail2news


# logging.basicConfig(level=logging.DEBUG)
class news2mail():
    """news to mail gateway class"""

    def __init__(self, verbose=False):
        self.wlfile = None
        self.logfile = None
        self.verbose = verbose

        self.sender = ''
        self.rcpt = ''
        self.envelope = ''

        self.smtpserver = 'localhost'

        self.hostname = gethostbyaddr(gethostname())[0]

        self.heads_dict = {}
        self.article, self.headers, self.body = [], [], []
        self.message = self.__addheads(
            email.message_from_file(sys.stdin, policy=email.policy.SMTP))

    def __addheads(self, msg):
        """add new header like X-Gateway: Received:
        """

        msg['X-Gateway'] = f'pyg {mail2news.__version__}' + \
            ' {mail2news.__description__}'

        # to make Received: header
        t = time.ctime(time.time())

        if time.daylight:
            tzone = time.tzname[1]
        else:
            tzone = time.tzname[0]

        # An example from debian-italian:
        # Received: from murphy.debian.org (murphy.debian.org [216.234.231.6])
        #        by smv04.iname.net (8.9.3/8.9.1SMV2) with SMTP id JAA26407
        #        for <kame.primo@innocent.com> sent by
        #        <debian-italian-request@lists.debian.org

        tmp = 'from GATEWAY by ' + self.hostname + \
            ' with pyg' + \
            '\n\tfor <' + self.rcpt + '> ; ' + \
            t + ' (' + tzone + ')\n'

        msg['Received'] = tmp

        return msg

    def __renameheads(self):
        """remove headers like Xref: Path: Lines:
           rename headers such as Newsgroups: to X-Newsgroups:

        headers renamed are useless or not rfc 822 copliant
        """
        try:
            if 'Newsgroups' in self.message:
                self.message['X-Newsgroups'] = \
                    self.message['Newsgroups']
                del self.message['Newsgroups']

            if 'NNTP-Posting-Host' in self.message:
                self.message['X-NNTP-Posting-Host'] = \
                    self.message['NNTP-Posting-Host']
                del self.message['NNTP-Posting-Host']
        except KeyError as ex:
            print(ex)

        try:
            # removing some others useless headers ....
            # that includes BOTH 'From ' and 'From'
            # 'Sender is usually set by INN, if ng is moderated...
            for key in ('Approved', 'From', 'Xref', 'Path', 'Lines', 'Sender'):
                if key in self.message:
                    del self.message[key]

            if 'Message-id' in self.message:
                msgid = self.message['Message-id']
                del self.message['Message-id']
                self.message['Message-Id'] = msgid
            else:
                # It should put a real user@domain
                self.heads_dict['Message-Id'] = 'pyg@puppapera.org'

            if 'References' in self.message and \
                    'In-Reply-To' not in self.message:
                refs = self.message['References'].split()
                self.message['In-Reply-To'] = refs[-1]

        except KeyError as message:
            print(message)

    def __sortheads(self):
        """make list sorting heads, Received: From: To: Subject: first,
           others, X-*, Resent-* last"""

        # put at top
        header_set = ('Received', 'From', 'To', 'Subject', 'Date')

        heads_dict = OrderedDict(self.message)
        for hdr in list(self.message.keys()):
            del self.message[hdr]

        for k in header_set:
            if k in heads_dict:
                self.message[k] = heads_dict[k]

        for k in heads_dict:
            if not k.startswith('X-') and not k.startswith('Resent-') \
                    and k not in header_set:
                self.message[k] = heads_dict[k]

        for k in heads_dict:
            if k.startswith('X-'):
                self.message[k] = heads_dict[k]

        for k in heads_dict:
            if k.startswith('Resent-'):
                self.message[k] = heads_dict[k]

    def process_message(self):
        """phase 3:
        format rfc 822 headers from input article
        """
        self.__renameheads()  # remove other heads
        self.__sortheads()

    def sendarticle(self):
        """Talk to SMTP server and try to send email."""
        s = smtplib.SMTP(self.smtpserver)
        s.set_debuglevel(self.verbose)

        s.sendmail(self.envelope, self.rcpt, self.message.as_bytes())

        s.quit()

def parse_cmdline(a_in):
    """
    set a dictionary with smtp new header in gw parameter (gw.smtpheads)
    return (test,verbose) boolean tuple
    """
    parser = argparse.ArgumentParser(
        description=f'pyg version {mail2news.__version__} - Copyright 2000 Cosimo Alfarano\n' + \
                    f'{mail2news.__description__}')

    parser.add_argument('-H', '--smtpserver', default='')
    parser.add_argument('-s', '--sender', required=True, default='')
    parser.add_argument('-e', '--envelope', default='')
    parser.add_argument('-t', '--to', dest='rcpt', required=True)
    parser.add_argument('-w', '--wlfile')
    parser.add_argument('-i', '--input', default='')
    parser.add_argument('-l', '--logfile')

    parser.add_argument('-T', '--test',
                        help='test mode (not send article via SMTP)',
                        action='store_true')
    parser.add_argument('-v', '--verbose', help='verbose output',
                        action='store_true')

    opts = parser.parse_args(a_in)

#  By rfc822 [Resent-]Sender: should be ever set, unless == From:
# (not this case). Should be a human, while [Resent-]From: may be a program.

    if opts.rcpt == '' or opts.sender == '':
        raise argparse.ArgumentError('missing command line option')

    if opts.envelope == '' and opts.sender != '':
        opts.envelope = opts.sender

    return opts

def main(args_in=None):
    """main is structured in 4 phases:
        1) check and set pyg's internal variables
        2) check whitelist for users' permission
        3) format rfc 822 headers from input article
        4) open smtp connection and send e-mail
    """

    """phase 1:
    check and set pyg's internal variables
    """
    out = ''

    # it returns only test, other parms are set directly in the actual
    # parameter
    if args_in is None:
        args_in = sys.argv[1:]
    args = parse_cmdline(args_in)

    n2m = news2mail(args)
    owner = None

    # check if n2m has some file prefercences set on commandline
    if args.wlfile is None:
        wl = os.path.expanduser(os.path.join(os.path.dirname(__file__),
                                             'pyg.whitelist'))
    else:
        wl = args.wlfile

    if args.logfile is None:
        log = os.path.expanduser(os.path.join(os.path.dirname(__file__),
                                              'pyg.log'))
    else:
        log = args.logfile

    wl = whitelist.whitelist(wl, log)

    """phase 2:
    check whitelist for user's permission
    """

    # make a first check of From: address
    owner = wl.checkfrom(n2m.message['From'])
    if owner is None:
        if sys.stdin.isatty() == 1 or args.test:
            out += str('"%s" is not in whitelist!' %
                       (n2m.message['From'][:-1])) + '\n'
        else:
            wl.logmsg(n2m.nntpheads, wl.DENY)

        # if verbose, I want to print out headers, so I can't
        # exit now.
        if not args.verbose:
            sys.exit(1)

    # Reformat the message
    n2m.process_message()

    # prints formatted email message only (without send) if user wants
    if args.verbose:
        out += n2m.message.as_string() + '\n'

    if owner is None:
        sys.exit(1)

    """phase 4:
    open smtp connection and send e-mail
    """

    wl.logmsg(n2m.heads_dict, wl.ACCEPT, owner)
    if not args.test:
        n2m.sendarticle()

    if args.input == '':
        print(out)
    else:
        return out
