import java.awt.Color;
import java.awt.Font;

import javax.swing.JFrame;
import javax.swing.JProgressBar;

public class ProgressBarDemo {
    
    JFrame frame = new JFrame();
    JProgressBar bar = new JProgressBar();

    ProgressBarDemo(){

        bar.setValue(0);
        bar.setBounds(0,0,420,100);
        bar.setStringPainted(true);
        bar.setFont(new Font("Verdana",Font.BOLD,20));
        bar.setForeground(Color.red);
        bar.setBackground(Color.BLACK);


        frame.add(bar);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(420,420);
        frame.setLayout(null);
        frame.setVisible(true);

        fill();

    }


    public void fill(){
        int counter = 0;

        while (counter<=100){
            bar.setValue(counter);
            try {
                Thread.sleep(15);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            counter += 1;
        }

        bar.setString("Done! :)");

        }
}
