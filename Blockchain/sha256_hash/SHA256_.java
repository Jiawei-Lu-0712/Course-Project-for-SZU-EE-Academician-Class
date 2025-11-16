package sha256_hash;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/*SHA256java库函数调用*/
public class SHA256_ {
    private String string;

    public SHA256_(String string) {
        this.string = string;
    }

    public String result() throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(string.getBytes());
        StringBuffer hexString = new StringBuffer();
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
