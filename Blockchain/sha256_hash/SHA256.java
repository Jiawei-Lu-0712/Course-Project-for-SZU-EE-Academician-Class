package sha256_hash;

/*SHA-256哈希算法实现*/
public class SHA256 {
    int repeat_num;// 512bit块数
    String msg_binary;
    StringBuffer str2 = new StringBuffer();// 定义一个动态长度字符串
    // 8个哈希初值，这里是对自然数中前8个质数（2，3，5，7，11，13，17，19）的平方根的小数部分取前32bit而来,第一个512Bit块的哈希初值
    String H0 = "6a09e667";
    String H1 = "bb67ae85";
    String H2 = "3c6ef372";
    String H3 = "a54ff53a";
    String H4 = "510e527f";
    String H5 = "9b05688c";
    String H6 = "1f83d9ab";
    String H7 = "5be0cd19";
    String A, B, C, D, E, F, G, H;//定义每个512bit块的哈希值，即将16进制的哈希初值转换成2进制

    String output = "";//最后的哈希值

    String[] k = new String[64];
    // 用到的64个混淆常量，是对自然数中前64个质数的立方根的小数部分取前32bit
    String[] K =
            {"428a2f98", "71374491", "b5c0fbcf", "e9b5dba5", "3956c25b", "59f111f1", "923f82a4", "ab1c5ed5",
                    "d807aa98", "12835b01", "243185be", "550c7dc3", "72be5d74", "80deb1fe", "9bdc06a7", "c19bf174",
                    "e49b69c1", "efbe4786", "0fc19dc6", "240ca1cc", "2de92c6f", "4a7484aa", "5cb0a9dc", "76f988da",
                    "983e5152", "a831c66d", "b00327c8", "bf597fc7", "c6e00bf3", "d5a79147", "06ca6351", "14292967",
                    "27b70a85", "2e1b2138", "4d2c6dfc", "53380d13", "650a7354", "766a0abb", "81c2c92e", "92722c85",
                    "a2bfe8a1", "a81a664b", "c24b8b70", "c76c51a3", "d192e819", "d6990624", "f40e3585", "106aa070",
                    "19a4c116", "1e376c08", "2748774c", "34b0bcb5", "391c0cb3", "4ed8aa4a", "5b9cca4f", "682e6ff3",
                    "748f82ee", "78a5636f", "84c87814", "8cc70208", "90befffa", "a4506ceb", "bef9a3f7", "c67178f2"};

    String[] w = new String[64];//定义64个字，每个字32Bit


    public SHA256(String msg) {
        /*
        *预处理
        对消息进行补位处理，使得最终长度是512的倍数，
        然后以512bit为单位对消息进行分块
        */
        for (int i = 0; i < 64; i++) {
            k[i] = hexToBi(K[i]);// 将K中64个常量从16进制转换成2进制
        }


        msg_binary = stringToBinary(msg);// 将要hash的字符串转换成二进制字符

        final int LENGTH = msg_binary.length();// 获取二进制字符串的长度,为一常量值

        // 判断待哈希的二进制字符串块数，每块512位
        if (LENGTH < 448)// 如果长度小于448
            repeat_num = 1;// 根据字符串长度判断总块数
        else if (LENGTH >= 448 && LENGTH <= 512)// 如果长度在448~512之间
            repeat_num = 2;
        else {
            if (LENGTH % 512 < 448)// 判断字符串长度在对512取模后的余数
                repeat_num = LENGTH / 512 + 1;
            else
                /*
                即使长度已经满足对512取模后余数是448，也需要补位，
                这种情况需要多补一个字符块，也就是512bit,即补位最少补1位，最多补512位
                 */
                repeat_num = LENGTH / 512 + 2;
        }

        char[] cw = new char[512 * repeat_num];// 新定义一个字符型数组，容量为512 * repeat_num，即为经过补位处理后的字符串

        for (int i = 0; i < LENGTH; i++) {// placing bits
            cw[i] = msg_binary.charAt(i);// 将该二进制字符串数据写入cw数组中
        }

        String str1 = Integer.toBinaryString(LENGTH);// 将字符串长度值转换成一个二进制字符串
        // 下面是对消息进行补位处理，使最终长度是512的倍数,最后64位是表示原始报文得到的二进制字符串的长度信息
        if (LENGTH < 448) {// 如果长度值小于448，
            cw[LENGTH] = '1';// 先补一个1
            for (int i = LENGTH + 1; i < 512 * repeat_num - str1.length(); i++) {// 后面补0
                cw[i] = '0';
            }
            for (int i = 512 * repeat_num - str1.length(); i < 512 * repeat_num; i++) {
                cw[i] = str1.charAt(i - 512 * repeat_num + str1.length());// 再补上原始报文得到的二进制字符串长度信息，总长度为512的倍数
            }
        }
        if (LENGTH >= 448 && LENGTH <= 512) {// 如果长度值为448~512，
            cw[LENGTH] = '1';// 先补一个1
            for (int i = LENGTH + 1; i < 512 * repeat_num - str1.length(); i++) {
                cw[i] = '0';// 后面补0
            }
            for (int i = 512 * repeat_num - str1.length(); i < 512 * repeat_num; i++) {
                cw[i] = str1.charAt(i - 512 * repeat_num + str1.length());
            }
        }
        if (LENGTH > 512) {// 长度值大于512，
            cw[LENGTH] = '1';// 先补一个1
            for (int i = LENGTH + 1; i < 512 * repeat_num - str1.length(); i++) {
                cw[i] = '0';// 后面补0
            }
            for (int i = 512 * repeat_num - str1.length(); i < 512 * repeat_num; i++) {
                cw[i] = str1.charAt(i - 512 * repeat_num + str1.length());
            }
        }


        str2 = str2.delete(0, str2.length());//  str2=null;
        for (int i = 0; i < 512 * repeat_num; i++) {
            str2 = str2.append(cw[i]);// 将cw这个二进制数组中的字符元素拼接为str2字符串，位数为512的整数倍
        }
        for (int n = 0; n < repeat_num; n++) {
            // w[0] to w[63]
            String str3;// 定义一个字符串，存储字符块，每个字符块512bit
            str3 = str2.substring(n * 512, (n + 1) * 512);// 截取字符块,每个块512bit，
        /*
        扩散过程
        对于消息分解成的每个512bit的块，需要构成64个字（每个字节是8位二进制数，每个字有4个字节，故每个字有32位）
         */
            for (int i = 0; i < 16; i++) {
                w[i] = str3.substring(i * 32, (i + 1) * 32);// 前16个字直接由原消息组成，记为w[0]...w[15]，每个字32bit
            }

            for (int i = 16; i < 64; i++) {// 剩下48个字由迭代公式计算而得
                // w[i] = w[i-16]+w[i-7]+S0+S1
                // 其中S1=smallSigmaOne(w[i - 2])，S0=smallSigmaZero(w[i-15])
                w[i] = Add(Add(smallSigmaOne(w[i - 2]), w[i - 7]), Add(smallSigmaZero(w[i - 15]), w[i - 16]));
            }
            // 将初始8个哈希值转化成二进制字符串，第二组512bit的数据的初始哈希值为前一组计算得出的H0~H7
            A = hexToBi(H0);
            B = hexToBi(H1);
            C = hexToBi(H2);
            D = hexToBi(H3);
            E = hexToBi(H4);
            F = hexToBi(H5);
            G = hexToBi(H6);
            H = hexToBi(H7);

            SHA_256(A, B, C, D, E, F, G, H);// 调用混淆函数，经过64轮迭代
        }
    }

    public String getHash() {// 获取最后hash值
        output = H0 + H1 + H2 + H3 + H4 + H5 + H6 + H7;// 最后一次计算合并H0~H7的值即为得到的哈希值
        return output;// 返回hash值
    }



















    // 计算A,B,C,D,E,F,G,H
    public String stringToBinary(String str) {// 将字符串转换成二进制字符串，每个字符用8位二进制数表示
        StringBuffer str2 = new StringBuffer();
        for (int i = 0; i < str.length(); i++) {
            str2 = str2.append(fillZero(Integer.toBinaryString(str.charAt(i)), 8));// 每个字符串用8位二进制数表示
        }
        return str2.toString();
    }

    public String fillZero(String str, int n) {// 补零函数，对长度小于n的二进制字符串，在其前面补零，使其长度达到n
        String str2 = "";
        StringBuffer str1 = new StringBuffer();

        if (str.length() < n)
            for (int i = 0; i < n - str.length(); i++) {
                str2 = str1.append('0').toString();
            }
        return str2 + str;
    }

    public String bit_df_or(String str1, String str2) {// 异或运算
        String str = new String();
        StringBuffer s = new StringBuffer();
        for (int i = 0; i < str1.length(); i++) {
            if (str1.charAt(i) == str2.charAt(i))// 判断等长度两个二进制字符串对应位置是否相等
                str = s.append('0').toString();// 相等取0
            else
                str = s.append('1').toString();// 不相等取1
        }
        return str;
    }

    // AND
    public String and(String str1, String str2) {// 与运算
        String str = new String();
        StringBuffer s = new StringBuffer();
        for (int i = 0; i < str1.length(); i++) {
            if (str1.charAt(i) == '0' || str2.charAt(i) == '0')
                str = s.append('0').toString();
            else
                str = s.append('1').toString();// 只有两二进制字符串对应位置都为1，结果才为1
        }
        return str;
    }

    // NOT
    public String not(String str1) {// 非运算
        String str = "";
        StringBuffer s = new StringBuffer();
        for (int i = 0; i < str1.length(); i++) {
            if (str1.charAt(i) == '0')
                str = s.append('1').toString();// 反运算，0变1，
            else
                str = s.append('0').toString();// 1变0
        }
        return str;
    }

    public void SHA_256(String A, String B, String C, String D, String E, String F, String G, String H) {// 迭代函数
        String temp1 = "";
        String temp2 = "";

        for (int i = 0; i < 64; i++) {// 经过64轮迭代
            // 迭代公式
            temp1 = T1(H, E, ch(E, F, G), w[i], k[i]);// T1
            temp2 = Add(temp1, T2(A, ma(A, B, C)));// T1+T2
            H = G;
            G = F;
            F = E;
            E = Add(D, temp1);// E=D+T1
            D = C;
            C = B;
            B = A;
            A = temp2;// A=(T1+T2)
        }
// 将迭代后最后一轮的A~H的值和初始哈希值相加，得到一个512bit块函数的摘要
        // 二进制转16进制
        H0 = biToHex(Add(A, hexToBi(H0)));
        H1 = biToHex(Add(B, hexToBi(H1)));
        H2 = biToHex(Add(C, hexToBi(H2)));
        H3 = biToHex(Add(D, hexToBi(H3)));
        H4 = biToHex(Add(E, hexToBi(H4)));
        H5 = biToHex(Add(F, hexToBi(H5)));
        H6 = biToHex(Add(G, hexToBi(H6)));
        H7 = biToHex(Add(H, hexToBi(H7)));

    }

    // rotate right n bits
    public String rotr(String str, int n) {// 循环右移函数
        return str.substring(str.length() - n) + str.substring(0, str.length() - n);
    }

    // right shift n bits
    public String shr(String str, int n) {// 向右移位，高位补0
        char[] fillZero = new char[n];
        for (int i = 0; i < fillZero.length; i++) {
            fillZero[i] = '0';
        }
        String str1 = str.substring(0, str.length() - n);
        return new String(fillZero) + str1;
    }

    // ADD
    public String Add(String str1, String str2) {// 二进制数相加运算
        char[] cArray = new char[32];
        int flag = 0;
        for (int i = str1.length() - 1; i >= 0; i--) {
            cArray[i] = (char) (((str1.charAt(i) - '0') + ((str2.charAt(i) - '0')) + flag) % 2 + '0');
            if (((str1.charAt(i) - '0') + (str2.charAt(i) - '0') + flag) >= 2)
                flag = 1;
            else
                flag = 0;
        }
        return new String(cArray);
    }

    public String ch(String str1, String str2, String str3) {
        // ch函数，Str1当前位为1，最终结果取str2的值，
        // 如果Str1当前位为0，结果取Str3的值
        return bit_df_or(and(str1, str2), and(not(str1), str3));// ch函数计算公式
    }

    public String ma(String str1, String str2, String str3) {// str1,str2,str3逐位比较，0多取0，1多取1
        return bit_df_or(bit_df_or(and(str1, str2), and(str1, str3)), and(str2, str3));// ma函数计算公式
    }

    public String smallSigmaZero(String str1) {
        // 即smallSigmaZero=ROTR7(str1)异或ROTR18(str1)异或SHR3(str1)，S0=smallSigmaZero(W[i-15])
        return bit_df_or(bit_df_or(rotr(str1, 7), rotr(str1, 18)), shr(str1, 3));
    }

    public String smallSigmaOne(String str1) {//S1=smallSigmaOne(W[i-2])
        // 即smallSigmaOne=ROTR17(str1)异或ROTR19(str1)异或SHR10(str1)
        return bit_df_or(bit_df_or(rotr(str1, 17), rotr(str1, 19)), shr(str1, 10));
    }

    public String bigSigmaZero(String str1) {// bigSigmaZero计算公式
        return bit_df_or(bit_df_or(rotr(str1, 2), rotr(str1, 13)), rotr(str1, 22));
    }

    public String bigSigmaOne(String str1) {// bigSigmaOne计算公式
        return bit_df_or(bit_df_or(rotr(str1, 6), rotr(str1, 11)), rotr(str1, 25));
    }

    public String biToHex(String str) {// 二进制转十六进制函数
        int temp = 0;
        StringBuffer st = new StringBuffer();

        for (int i = 0; i < str.length() / 4; i++) {
            temp = Integer.valueOf(str.substring(i * 4, (i + 1) * 4), 2);
            st = st.append(Integer.toHexString(temp));
        }
        return st.toString();
    }

    public String hexToBi(String str) {// 十六进制转二进制函数
        String temp = "";
        String st = "";

        for (int i = 0; i < str.length(); i++) {
            switch (str.charAt(i)) {// 获取第i个字符，将16进制转换成相应的2进制
                case '0':
                    st = "0000";
                    break;
                case '1':
                    st = "0001";
                    break;
                case '2':
                    st = "0010";
                    break;
                case '3':
                    st = "0011";
                    break;
                case '4':
                    st = "0100";
                    break;
                case '5':
                    st = "0101";
                    break;
                case '6':
                    st = "0110";
                    break;
                case '7':
                    st = "0111";
                    break;
                case '8':
                    st = "1000";
                    break;
                case '9':
                    st = "1001";
                    break;
                case 'a':
                    st = "1010";
                    break;
                case 'b':
                    st = "1011";
                    break;
                case 'c':
                    st = "1100";
                    break;
                case 'd':
                    st = "1101";
                    break;
                case 'e':
                    st = "1110";
                    break;
                case 'f':
                    st = "1111";
                    break;
            }
            temp = temp + st;
        }
        return temp;// 将字符串转换成二进制串返回
    }

    // T1
    /*
    T1=H+bigSigmaOne+ch+ki+wi
     */
    public String T1(String str_h, String str_e, String str_ch, String str_w, String str_k) {// T1函数
        // T1=H+bigSigmaOne(str_e)+ch+ki+wi
        return Add(Add(Add(str_h, bigSigmaOne(str_e)), Add(str_ch, str_w)), str_k);
    }

    // T2
    /*
    T2=bigSigmaZero+ma
     */
    public String T2(String str_a, String str_ma) {// T2函数
        return Add(bigSigmaZero(str_a), str_ma);
    }

}






