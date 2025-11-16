package sha256_hash;

import java.security.NoSuchAlgorithmException;
import java.util.Scanner;
/*无界面，命令行输入，别输入中文，中文因为编码方式不一致，得到的哈希结果不一致。*/
public class Test {
    public static void main(String[] args) throws NoSuchAlgorithmException {
        while (true) {
            Scanner scanner = new Scanner(System.in);
            System.out.println("请输入字符串，按回车结束:");
            String a = scanner.next();
            String sha256 = new SHA256(a).getHash();
            System.out.println("SHA256算法结果:" + sha256);
            SHA256_ example = new SHA256_(a);
            System.out.println("调用库函数实现结果:" + example.result());
            System.out.println("验证结果:" + sha256.equals(example.result()));
        }
    }
}
