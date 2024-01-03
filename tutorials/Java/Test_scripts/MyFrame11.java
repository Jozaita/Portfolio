import javax.swing.JFrame;

public class MyFrame11 extends JFrame {
    
    DragPanel dragPanel = new DragPanel();

    MyFrame11(){

        this.add(dragPanel);
        this.setTitle("Drag and Drop demo");
        this.setSize(600,600);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setVisible(true);
    }
}
