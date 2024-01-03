public class MyGenericClass <T,V> {

    T x;
    V y;

    MyGenericClass(T x){
        this.x = x;
        this.y = y;
    }

    public V getValue(){
        return y;
    }
    
}
