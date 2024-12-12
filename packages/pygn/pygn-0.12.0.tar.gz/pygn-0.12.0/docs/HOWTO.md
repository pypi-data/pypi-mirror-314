MUST BE FINISHED!


It is a (very) small HOWTO to make pyg working properly.

pygm2n:

Pre: a fully working MTA (ie postfix) where you can run procmail or any other MDA. 
A news server (local or remote) where you can create groups (admin
privileges).

Create a user, ie mailgate, set its procmail as:

:0 bhc:
| pygm2n -n local.test

or its maildrop (thanks to Joy):

dotlock pygm2n.`echo $$`.lock {
  `pygm2n -n local.test`
}

you can use -a your@address and -s nntphost if local.test is moderated,
or nntphost isn't localhost

[NOTE: if you've configuration for any other MDA, please file a wishlist
bug against pyg]

Create local.test (if it doen't exist).

Now any mail you will write to mailgate user, will be sent to the
server. Read local.test on localhost (or nntphost), you will see
message.
