public abstract class Vehicle {
    double speed;

    abstract void greet();
    //Abstract methods are not implemented, but in their children

    void go(){
        System.out.println("This vehicle is moving");
    }
    
    void stop(){
        System.out.println("This vehicle has been stopped");
    } 
    
}
