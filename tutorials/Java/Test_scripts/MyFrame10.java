import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JFrame;
import javax.swing.JLabel;

public class MyFrame10 extends JFrame implements MouseListener {

    JLabel label;

    MyFrame10 (){
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setLayout(null);
        this.setSize(500, 500);

        label = new JLabel();
        label.setBounds(0,0,100,100);
        label.setBackground(Color.red);
        label.setOpaque(true);

        label.addMouseListener(this); 
        
        this.add(label);
        this.setVisible(true);

    }

    @Override
    public void mouseClicked(MouseEvent e) {
        System.out.println("You clicked the mouse!");    
    }

    @Override
    public void mouseEntered(MouseEvent e) {
       System.out.println("You entered the component!"); 
    }

    @Override
    public void mouseExited(MouseEvent e) {
       System.out.println("You exited the component!"); 
    }

    @Override
    public void mousePressed(MouseEvent e) {
        System.out.println("You pressed the mouse!");  
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        System.out.println("You released the mouse!"); 
    }

   

}