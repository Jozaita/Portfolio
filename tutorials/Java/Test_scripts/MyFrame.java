import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JTextField;

public class MyFrame extends JFrame implements ActionListener {

    JButton button;
    JTextField textField;

    MyFrame(){
        this.setTitle("TITLE GOES HERE");
        this.setDefaultCloseOperation(this.EXIT_ON_CLOSE);  
        this.setSize(420, 420);
        this.setLayout(new FlowLayout());
        ImageIcon image = new ImageIcon("sombrero_azul.png");
        this.setIconImage(image.getImage());

        button = new JButton("SUBMIT");
        button.addActionListener(this);

        textField = new JTextField();
        textField.setPreferredSize(new Dimension(250, 40));
        textField.setFont(new Font("Consolas",Font.PLAIN,20 ));
        textField.setForeground(new Color(0x00FF00));
        textField.setBackground(Color.black);
        textField.setCaretColor(Color.white);
        textField.setText("username");
        //textField.setEditable(false);



        this.add(button);
        this.add(textField);


        this.pack();
        this.setVisible(true);

        //this.getContentPane().setBackground(Color.GRAY);
        //this.getContentPane().setBackground(new Color(255,255,255));}
    }
    @Override
    public void actionPerformed(ActionEvent e) {
       if (e.getSource() == button){
        String text = textField.getText();
        System.out.println("MESSAGE: "+ text);
        button.setEnabled(false);
        textField.setEditable(false);
       }
    
}

}
