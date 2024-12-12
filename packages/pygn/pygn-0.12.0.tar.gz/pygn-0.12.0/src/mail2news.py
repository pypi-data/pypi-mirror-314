"""Mail to news gateway script. Copyright 2000 Cosimo Alfarano

Author: Cosimo Alfarano
Date: September 16 2000

mail2news.py - (C) 2000 by Cosimo Alfarano <Alfarano@Students.CS.UniBo.It>
You can use this software under the terms of the GPL. If we meet some day,
and you think this stuff is worth it, you can buy me a beer in return.

Thanks to md for this useful formula. Beer is beer.

Gets news email and sends it via SMTP.

class mail2news is  hopefully conform to rfc850.

"""
import argparse
import io
from collections import OrderedDict
import email
import email.policy
import logging
try:
    import nntplib
except (ImportError, ModuleNotFoundError):
    import nntp as nntplib
import os
from re import findall
from socket import gethostbyaddr, gethostname
import sys
import tempfile


#logging.basicConfig(level=logging.DEBUG)
# This is the single source of Truth
# Yes, it is awkward to have it assymetrically here
# and not in news2mail as well.
__version__ = '0.12.0'
__description__ = 'The Python Gateway Script: news2mail mail2news gateway'


class mail2news(object):
    """news to mail gateway class"""

    def __init__(self, options):
        #    newsgroups = None  # Newsgroups: local.test,local.moderated...
        #    approved = None  # Approved: kame@aragorn.lorien.org
        if 'NNTPHOST' in os.environ:
            self.newsserver = os.environ['NNTPHOST']
        else:
            self.newsserver = 'localhost'

        self.port = 119
        self.user = None
        self.password = None
        self.verbose = options.verbose
        logging.debug('self.verbose = %s', self.verbose)

        self.hostname = gethostbyaddr(gethostname())[0]

        self.heads_dict, self.smtpheads, self.nntpheads = {}, {}, {}
        if options.input == '':
            self.message = self.__readfile(options, sys.stdin)
        else:
            with open(options.input, 'r') as inp_stream:
                self.message = self.__readfile(options, inp_stream)

        self.message['X-Gateway']=f'pyg {__version__} {__description__}'

    def __add_header(self, header, value, msg=None):
        if msg is None:
            msg = self.message
        if value:
            msg[header] = value.strip()

    def __readfile(self, opt, input_stream):
        message = email.message_from_file(input_stream,
                                          policy=email.policy.SMTP)

        if (len(message) == 0) \
                and message.get_payload().startswith('/'):
            msg_file_name = message.get_payload().strip()
            del message
            with open(msg_file_name, 'r') as msg_file:
                message = email.message_from_file(msg_file,
                                                  policy=email.policy.SMTP)

        # introduce nntpheads
        self.__add_header('Newsgroups', opt.newsgroup, message)
        self.__add_header('Approved', opt.approver, message)

        return message

    def renameheads(self):
        """rename headers such as Resent-*: to X-Resent-*:

        headers renamed are useless or not rfc 977/850 copliant
        handles References/In-Reply-To headers
        """
        try:

            for key in list(self.message.keys()):
                if key.startswith('Resent-'):
                    if ('X-' + key) in self.message:
                        self.message['X-Original-' + key] = \
                            self.message['X-' + key]
                    self.message['X-' + key] = self.message[key]
                    del self.message[key]

            # In rfc822 References: is considered, but many MUA doen't put it.
            if ('References' not in self.message) and \
                    ('In-Reply-To' in self.message):
                print(self.message['In-Reply-To'])

                # some MUA uses msgid without '<' '>'
#                ref = findall('([^\s<>\']+@[^\s<>;:\']+)', \
                # but I prefer use RFC standards
                ref = findall('(<[^<>]+@[^<>]+>)',
                              self.message['In-Reply-To'])

                # if found, keep first element that seems a Msg-ID.
                if (ref and len(ref)):
                    self.message['References'] = f'{ref[0]}\n'

        except KeyError as message:
            print(message)

    def removeheads(self, heads=None):
        """remove headers like Xref: Path: Lines:
        """

        try:
            # removing some others useless headers .... (From is not From:)

            rmheads = ['Received', 'From ', 'NNTP-Posting-Host',
                       'X-Trace', 'X-Compliants-To', 'NNTP-Posting-Date']
            if heads:
                rmheads.append(heads)

            for head in rmheads:
                if head in self.message:
                    del self.message[head]

            if 'Message-Id' in self.message:
                msgid = self.message['Message-Id']
                del self.message['Message-Id']
                self.message['Message-Id'] = msgid
            else:
                msgid = '<pyg.{os.getpid()}@tuchailepuppapera.org>\n'
                self.message['Message-Id'] = msgid

        except KeyError as message:
            print(message)

    def sortheads(self):
        """make list sorted by heads: From: To: Subject: first,
           others, X-*, X-Resent-* last"""

        heads_dict = OrderedDict(self.message)
        for hdr in list(self.message.keys()):
            del self.message[hdr]

        # put at top
        head_set = ('Newsgroups', 'From', 'To', 'X-To', 'Cc', 'Subject',
                    'Date', 'Approved', 'References', 'Message-Id')

        logging.debug('heads_dict = %s', heads_dict)
        for k in head_set:
            if k in heads_dict:
                self.__add_header(k, heads_dict[k])

        for k in heads_dict:
            if not k.startswith('X-') and not k.startswith('X-Resent-') \
                    and k not in head_set:
                self.__add_header(k, heads_dict[k])

        for k in heads_dict:
            if k.startswith('X-'):
                self.__add_header(k, heads_dict[k])

        for k in heads_dict:
            if k.startswith('X-Resent-'):
                self.__add_header(k, heads_dict[k])

    def sendemail(self):
        "Talk to NNTP server and try to send email."
        # readermode must be True, otherwise we don't have POST command.
        server = nntplib.NNTP(self.newsserver, self.port, self.user,
                              self.password, readermode=True)

        logging.debug('self.verbose = %s', self.verbose)
        if self.verbose:
            server.set_debuglevel(2)

        msg_bytes = self.message.as_bytes()
        try:
            server.post(io.BytesIO(msg_bytes))
        except UnicodeEncodeError:
            with tempfile.NamedTemporaryFile(suffix="eml", prefix="failed_msg",
                                             delete=False) as tmpf:
                tmpf.write(msg_bytes)
                logging.info("failed file name = %s", tmpf.name)
            logging.exception("Failed to convert message!")

        server.quit()

def parse_cmdline(arg_in):
    parser = argparse.ArgumentParser(
        description=f'pyg version {__version__} - Copyright 2000 Cosimo Alfarano' + \
            f'\n{__description__}')

    parser.add_argument('-s', '--newsserver', default='')
    parser.add_argument('-a', '--approver', default='',
                        help="address of moderator/approver")
    parser.add_argument('-n', '--newsgroup', default='',
                        help='newsgroup[s] (specified as comma separated ' +
                        'without spaces list)', required=True)
    parser.add_argument('-u', '--user', default='',
                        help='NNTP server user (for authentication)')
    parser.add_argument('-p', '--password', default='',
                        help='NNTP server password (for authentication)')
    parser.add_argument('-P', '--port', default='')
    parser.add_argument('-e', '--envelope', default='')
    parser.add_argument('-i', '--input', default='')
    parser.add_argument('-l', '--logfile')

    parser.add_argument('-T', '--test', action='store_true',
                        help='test mode (not send article via NNTP)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose output ' +
                        '(usefull with -T option for debugging)')

    args = parser.parse_args(arg_in)

    if not args.newsgroup:
        raise argparse.ArgumentError('Error: Missing Newsgroups\n')

    return args


def main(args_in=None):
    """main is structured in 4 phases:
        1) check and set pyg's internal variables
        2) check whitelist for users' permission
        3) format rfc 822 headers from input article
        4) open smtp connection and send e-mail
    """
    out = ''

    try:
        """phase 1:
        check and set pyg's internal variables
        """
        if args_in is None:
            args_in = sys.argv[1:]
        opt = parse_cmdline(args_in)

        m2n = mail2news(opt)
        # owner = None

        """phase 3:
        format rfc 822 headers from input article
        """
        m2n.renameheads()    # rename useless heads
        m2n.removeheads()    # remove other heads

        m2n.sortheads()        # sort remaining heads :)

        if opt.verbose:
            out += m2n.message.as_string() + '\n'

        logging.debug('m2n.payload = len %d', len(m2n.message.get_payload()))
        if len(m2n.message.get_payload()) > 0:
    #        wl.logmsg(m2n.heads_dict,wl.ACCEPT,owner)
            if not opt.test:
                try:
                    m2n.sendemail()
                except nntplib.NNTPError as ex:
                    logging.exception(ex)
    except KeyboardInterrupt:
        logging.error('Keyboard Interrupt')
        sys.exit(0)

    if opt.input == '':
        print(out)
    else:
        return out
