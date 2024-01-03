public class Car4 {
    private String make;
    private String model;
    private int year; 

    Car4(String make, String model, int year){
            this.setMake(make);
            this.setModel(model);
            this.setYear(year);
    }

    Car4(Car4 x){
        this.copy(x);
    }

    public String getMake(){
        return make;
    }

    public String getModel(){
        return model;
    }

    public int getYear(){
        return year;
    }

    public void setMake(String val){
        this.make = val;
    }

    public void setModel(String val){
        this.model = val;
    }

    public void setYear(int val){
        this.year = val;
    }

    public void copy(Car4 x){
        this.setMake(x.getMake());
        this.setModel(x.getModel());
        this.setYear(x.getYear());
    }
}
