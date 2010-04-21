# Sieve Script by Alice Bevan-McGregor <alice@gothcandy.com>
# For server-side filtering of mailing lists, bulk traffic, self-BCCs, and vacation time.
# Spam is dealt with by Amavis and an extensive list of plugins automatically.
#
# Excessive use of elsif to remove the need for the 'stop' statement.
#
# Note: Should use address :domain :is instead of address: contains.

require ["fileinto", "include", "imapflags", "regex", "relational", "comparator-i;ascii-numeric", "envelope", "subaddress"];


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

# Filter + notation sub-addressing.
} elsif envelope :detail "to" "mvp" {
        fileinto "Projects.MVP";

# Filter clients into appropriate mailboxes.
} elsif address :domain :is "From" "campbellriver.ca" {
        fileinto "Clients.City of Campbell River";
} elsif address :domain :is "From" "comoxvalleychamber.com" {
        fileinto "Clients.Comox Valley Chamber of Commerce";
} elsif address :domain :is "From" "chameleoncreative.com" {
        fileinto "Clients.Chameleon Creative";
} elsif address :domain :is "From" ["comoxrecreation.com", "active.com"] {
        fileinto "Clients.Comox Recreation Commission";
} elsif address :domain :is "From" "comoxvalleyartgallery.com" {
        fileinto "Clients.Comox Valley Art Gallery";
} elsif address :domain :is "From" "compassadventure.ca" {
        fileinto "Clients.Compass Adventure";
} elsif address :domain :is "From" "davidphoto.ca" {
        fileinto "Clients.David Morris Photography";
} elsif address :domain :is "From" "gmeco.ca" {
        fileinto "Clients.GME";
} elsif address :domain :is "From" "57aromas.com" {
        fileinto "Clients.Green Valley Aromatherapy";
} elsif address :domain :is "From" ["healinghandsvictoria.com", "healinghandstraining.com", "healinghandsmassage.com"] {
        fileinto "Clients.Healing Hands";
} elsif address :domain :is "From" "ilscorp.com" {
        fileinto "Clients.ILS Learning Corporation";
} elsif address :domain :is "From" "infostation.ca" {
        fileinto "Clients.Information Station";
} elsif address :domain :is "From" ["infilm.ca", "inlocation.ca"] {
        fileinto "Clients.Island North Film Commission";
} elsif address :domain :is "From" ["medinet.ca", "oscarwest.com", "seawatchmedical.ca"] {
        fileinto "Clients.Medical Clinics and Pharmacies";
} elsif address :domain :is "From" ["nelsonroofing.com", "camair.ca"] {
        fileinto "Clients.Nelson Roofing and Sheet Metal";
} elsif address :domain :is "From" "niefs.net" {
        fileinto "Clients.NIEFS";
} elsif address :domain :is "From" "stolenmomentsphotography.com" {
        fileinto "Clients.Stolen Moments Photography";
} elsif address :domain :is "From" "comox.ca" {
        fileinto "Clients.Town of Comox";


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
} elsif header :contains "List-Id" "paste-users.googlegroups.com" {
        fileinto "Projects.Paste";
} elsif header :contains "List-Id" "oscarmcmaster-bc-users.lists.sourceforge.net" {
        fileinto "Projects.Oscar";
} elsif header :contains "List-Id" "oscarmcmaster-devel.lists.sourceforge.net" {
        fileinto "Projects.Oscar";
} elsif address :is "Sender" "tunecouncil@tunecouncil.talklist.com" {
        fileinto "Projects.TuneCore Council";


# Annoying mailing lists.  TBD.
# } elsif header :contains "From" [] {
#        reject "I have tried to unsubscribe; I do not want your newsletter.  Please unsubscribe me."


# I BCC my replies for better archiving, but I wrote it, so I don't need to read it.
} elsif address "Return-Path" ["alice@gothcandy.com", "mbevan@topfloor.ca", "amcgregor@topfloor.ca"] {
        setflag "\\seen";

# TODO: Soft-bounce (but still deliver) mail to old aliases like matt.bevan@topfloor.ca.

# Vacation mail.
# I don't want vacation messages going to mailing lists, etc. thus this is an elsif.
#} elsif header :regex "date" "(June (2[4-9]|30)|July [1-7]) 2009" {
#        include :personal "vacation.sieve";
#        
#        # Redirect important e-mail to my mobile push account.
#        if header :value "lt" :comparator "i;ascii-numeric" "X-Priority" "3" {
#                redirect "alice.mcgregor@me.com";
#        }
#    
} else {
        keep;
}
