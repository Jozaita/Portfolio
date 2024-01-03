
import java.awt.Color;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JButton;

import javax.swing.JFrame;
import javax.swing.JLabel;

public class MyFrame9 extends JFrame implements KeyListener {

    JLabel label;

    MyFrame9(){
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(500, 500);
        this.setLayout(null);
        this.addKeyListener(this);

        label = new JLabel();
        label.setBounds(0,0,100,100);
        label.setBackground(Color.red);
        label.setOpaque(true);
        
        this.add(label);
        this.setVisible(true);
    }

    @Override
    public void keyPressed(KeyEvent e) {
        switch(e.getKeyChar()){
            case 37:label.setLocation(label.getX()-5, label.getY());
            break;
            case 38:label.setLocation(label.getX(), label.getY()-5);
            break;
            case 39:label.setLocation(label.getX(), label.getY()+5);
            break;
            case 40:label.setLocation(label.getX()+5, label.getY());
            break;
        }
        
    }

    @Override
    public void keyReleased(KeyEvent e) {
      System.out.println("You released key character: "+e.getKeyChar());
      System.out.println("You released key code: "+e.getKeyCode());
    }

    @Override
    public void keyTyped(KeyEvent e) {
        switch(e.getKeyChar()){
            case 'a':label.setLocation(label.getX()-5, label.getY());
            break;
            case 'w':label.setLocation(label.getX(), label.getY()-5);
            break;
            case 's':label.setLocation(label.getX(), label.getY()+5);
            break;
            case 'd':label.setLocation(label.getX()+5, label.getY());
            break;
        }
       
    }


}