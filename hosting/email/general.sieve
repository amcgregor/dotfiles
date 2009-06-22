# Sieve Script by Alice Bevan-McGregor <alice@gothcandy.com>
# For server-side filtering of mailing lists, bulk traffic, self-BCCs, and vacation time.
# Spam is dealt with by Amavis and an extensive list of plugins automatically.
#
# Excessive use of elsif to remove the need for the 'stop' statement.
#
# Note: Should use address :domain :is instead of address: contains.

require ["fileinto", "include", "imapflags", "regex", "relational", "comparator-i;ascii-numeric"];


# Blacklist e-mail addresses.  TBD.
# if header :contains "from" [] {
#         discard;
#         stop;
# }


# Filter OEM supplier messages.
if address :domain :is "From" ["ncix.com", "ncix.net", "pecanada.com", "semicom.ca"] {
        fileinto "Suppliers";

# Filter ISPs and hosting providers.
} elsif address :domain :is "From" ["amazon.com", "zoneedit.com", "domainsatcost.ca"] {
        fileinto "Hosting";

# Filter music production resources.
} elsif address :domain :is "From" "tunecore.com" {
        fileinto "Projects.Music Production";

# Apple sends receipts for the "purchase" of free items.
} elsif allof ( address :contains "From" "do_not_reply@apple.com",
                header :contains "Subject" "Your receipt" ) {
        fileinto "Receipts";


# Mailing list traffic filters.

} elsif header :contains "List-Id" "turbogears" {
        fileinto "Projects.TurboGears";

} elsif header :contains "List-Id" "pylons-discuss.googlegroups.com" {
        fileinto "Projects.Pylons";

} elsif header :contains "List-Id" "webpy.googlegroups.com" {
        fileinto "Projects.Webpy";

} elsif header :contains "List-Id" "cv-web-posse.googlegroups.com" {
        fileinto "Projects.CV Web Posse";

} elsif header :contains "List-Id" "turbomail-devel.googlegroups.com" {
        fileinto "Projects.TurboMail";


# Annoying mailing lists.  TBD.
# } elsif header :contains "From" [] {
#        reject "I have tried to unsubscribe; I do not want your newsletter.  Please unsubscribe me."


# I BCC my replies for better archiving, but I wrote it, so I don't need to read it.
} elsif address "Return-Path" ["alice@gothcandy.com", "mbevan@topfloor.ca"] {
        setflag "\\seen";


# Vacation mail.
# I don't want vacation messages going to mailing lists, etc. thus this is an elsif.
} elsif header :regex "date" "(June (2[4-9]|30)|July [1-7]) 2009" {
        include :personal "vacation.sieve";
        
        # Redirect important e-mail to my mobile push account.
        if header :value "lt" :comparator "i;ascii-numeric" "X-Priority" "3" {
                redirect "alice.mcgregor@me.com";
        }
    
} else {
        keep;
}
