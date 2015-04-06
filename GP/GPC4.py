#gs presence server (29900)
#based on works: prmasterserver, gsopensdk
#
#
#ONE TCP SERVER SOCKET BASE
#Session number bundled with socket instance
#ONE DATABASE FOR USER INFORMATION
#CHALLENGE DECODING PROCEDURE
#PASSWORD ENCODING/DECODING, MD5-HASHING PROCEDURES
##<|lc\1 <- (login or newuser)
##>|login -> lc\2
##>|newuser -> nur
##<|bdy,blk,bm
##>|getprofile -> pi
##>|status ->bdy,blk,bm
##?|lt
##?|ka
