import hashlib
import hmac

def MS( skey , message ):

    #
    skey = bytes( skey, 'UTF-8' )
    message = bytes( message, 'UTF-8' )

    #
    digester = hmac.new( skey, message, hashlib.sha512 )
    sign = digester.hexdigest()

    #
    return sign
