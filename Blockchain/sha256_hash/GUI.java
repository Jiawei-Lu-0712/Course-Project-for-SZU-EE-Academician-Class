package sha256_hash;

/*
 * 界面程序
 * 对txt文本文件取哈希，文本文件也不要出现非ASCII字符，文本文件直接拖进文本框就行了。
 * 图片取哈希只支持jpg和png格式的图片。直接拖进文本框就行了。
 */

import javax.swing.*;
import java.awt.*;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DropTargetDropEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.nio.file.Files;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Objects;
import java.util.Scanner;

public class GUI extends JPanel {
    public static void main(String[] args) {
        int x = 1000;
        int y = 1000;
        JFrame frame = new JFrame("SHA256哈希计算器");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(new SHA256Panel());
        frame.setSize(x, y);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setVisible(true);

    }
}

class SHA256Panel extends JPanel {
    private JButton calcButton = new JButton("计算");
    private JButton clearButton = new JButton("清空");
    private JButton verifyButton = new JButton("验证");
    private JTextArea input = new JTextArea();
    private JTextField output1 = new JTextField("");
    private JTextField output2 = new JTextField("");
    private JTextField output3 = new JTextField("");

    private SHA256 SHA;
    ButtonListener listener = new ButtonListener();
    ButtonListener2 listener2 = new ButtonListener2();
    ButtonListener3 listener3 = new ButtonListener3();

    public SHA256Panel() {
        JScrollPane jsp = new JScrollPane(input);
        jsp.setBounds(960, 30, 20, 550);
        jsp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        jsp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);

        add(jsp);
        input.setLineWrap(true);
        input.setWrapStyleWord(true);
        input.setBorder(BorderFactory.createLineBorder(Color.decode("#2C6791")));
        calcButton.setFont(new Font("微软雅黑", 1, 22));
        calcButton.setBounds(430, 600, 120, 60);
        calcButton.addActionListener(listener);
        calcButton.setFocusPainted(false);
        clearButton.setFont(new Font("微软雅黑", 1, 22));
        clearButton.setBounds(50, 600, 120, 60);
        clearButton.addActionListener(listener2);
        clearButton.setFocusPainted(false);
        verifyButton.setFont(new Font("微软雅黑", 1, 22));
        verifyButton.setBounds(790, 600, 120, 60);
        verifyButton.addActionListener(listener3);
        verifyButton.setFocusPainted(false);
        setLayout(null);// clear layout
        add(calcButton);
        add(clearButton);
        add(verifyButton);
        add(input);
        add(output1);
        add(output2);
        add(output3);
        input.setBounds(30, 30, 925, 550);
        input.setText("Input message here:");
        input.setCaretPosition(input.getDocument().getLength());
        JScrollBar verticalScrollBar = jsp.getVerticalScrollBar();
        verticalScrollBar.setValue(verticalScrollBar.getMaximum());
        input.setFont(new Font("微软雅黑", Font.PLAIN, 25));
        input.setDropTarget(new FileDropTarget());

        output1.setBounds(30, 680, 900, 60);
        output2.setBounds(30, 760, 900, 60);
        output3.setBounds(30, 840, 900, 60);
        output1.setFont(new Font("Arial", Font.PLAIN, 25));
        output2.setFont(new Font("Arial", Font.PLAIN, 25));
        output3.setFont(new Font("微软雅黑", Font.PLAIN, 25));
        setVisible(true);
    }

    private class ButtonListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            SHA = new SHA256(input.getText());
            SHA256_ sha256d = new SHA256_(input.getText());
            output1.setText(SHA.getHash());
            try {
                output2.setText(sha256d.result());
            } catch (NoSuchAlgorithmException ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    private class ButtonListener2 implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            input.setText("");
            output1.setText("");
            output2.setText("");
            output3.setText("");
        }
    }

    private class ButtonListener3 implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            SHA256_ sha256d = new SHA256_(input.getText());
            try {
                output3.setText(String.valueOf(Objects.equals(sha256d.result(), SHA.getHash())));
            } catch (NullPointerException | NoSuchAlgorithmException ex) {
                output3.setText("请先计算哈希！");
            }
        }
    }

    private class FileDropTarget extends DropTarget {
        @Override
        public synchronized void drop(DropTargetDropEvent event) {
            try {
                Transferable transferable = event.getTransferable();
                if (transferable.isDataFlavorSupported(DataFlavor.javaFileListFlavor)) {
                    event.acceptDrop(DnDConstants.ACTION_COPY);
                    java.util.List<File> fileList = (java.util.List<File>) transferable.getTransferData(DataFlavor.javaFileListFlavor);
                    // 处理每一个文件
                    for (File file : fileList) {
                        //支持读取.jpg和.png的图片
                        if (file.getName().toLowerCase().endsWith(".jpg") || file.getName().toLowerCase().endsWith(".png")) {
                            byte[] filebytes = Files.readAllBytes(file.toPath());
                            String base64String = Base64.getEncoder().encodeToString(filebytes);
                            input.setText(base64String);
                            input.setCaretPosition(input.getDocument().getLength());


                        } else if (file.getName().toLowerCase().endsWith(".txt")) {//支持读取.txt文件
                            Scanner scanner = new Scanner(file.toPath());
                            String content = "";
                            while (scanner.hasNextLine()) {
                                content += scanner.nextLine() + "\n";
                            }
                            scanner.close();
                            input.setText(content);
                            input.setCaretPosition(input.getDocument().getLength());
                        }
                        else {
                            output3.setText("不支持该类型的哈希值计算!");
                        }
                    }
                }
            } catch (Exception e) {
                output3.setText("不支持该类型的哈希值计算!");
            }
        }
    }
}

