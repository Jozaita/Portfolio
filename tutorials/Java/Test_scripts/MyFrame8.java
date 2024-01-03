import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
 

import javax.swing.JButton;
import javax.swing.JColorChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class MyFrame8 extends JFrame implements ActionListener {

    JButton button;
    JLabel label;

    MyFrame8(){
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setLayout(new FlowLayout());

        button = new JButton("Pick a color");
        button.addActionListener(this);

        label = new JLabel();
        label.setBackground(Color.LIGHT_GRAY);
        label.setText("This is some text");
        label.setFont(new Font("Times new roman",Font.PLAIN,24));
        
        this.add(button);
        this.add(label);
        this.pack();
        this.setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
            if (e.getSource() == button){
                JColorChooser colorChooser = new JColorChooser();
                Color color = JColorChooser.showDialog(null,"COLORS",Color.red);
                label.setForeground(color);
            }
    
    }

}