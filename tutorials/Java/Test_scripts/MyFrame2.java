import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class MyFrame2 extends JFrame implements ActionListener {
    JButton button;
    JLabel label;

    MyFrame2(){

        ImageIcon icon = new ImageIcon("logo.png");
        ImageIcon icon2 = new ImageIcon("logo.png"); 

        label = new JLabel();
        label.setIcon(icon2);
        label.setBounds(150, 250, 150, 150);
        label.setVisible(false);

        
        button = new JButton();
        button.setBounds(200, 100, 250, 100);
        button.addActionListener(this);
        button.setText("Receive a greeting");
        button.setFocusable(false);
        button.setIcon(icon);
        button.setHorizontalTextPosition(JButton.CENTER);
        button.setVerticalTextPosition(JButton.BOTTOM);
        button.setFont(new Font("Comic Sans",Font.ITALIC,20));
        button.setIconTextGap(-10);
        button.setForeground(Color.RED);
        button.setBackground(Color.BLACK);
        button.setBorder(BorderFactory.createEtchedBorder());
        //button.setEnabled(false);
        //button.addActionListener(e -> System.out.println("Hi!"));
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setLayout(null);
        this.setSize(500,500);
        this.setVisible(true);
        this.add(button);
        this.add(label);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == button){
            System.out.println("Hi!");
            label.setVisible(true);

    }
        
    }
    
}
