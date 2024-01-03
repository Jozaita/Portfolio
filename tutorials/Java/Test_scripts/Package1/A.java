package Package1;
import Package2.*;

public class A {

    static protected String protectedMessage = "This is protected";
    public static void main(String[] args){
        B b = new B();
        System.err.println(b.privateMessage);
        //C c = new C();
        //System.out.println(c.defaultMesage);
        //System.out.println(c.publicMessage);

    }
}
