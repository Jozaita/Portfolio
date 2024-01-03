public class Car {
 String make = "Chevrolet";   
 String model = "Corvette";
 int year = 2020;
 String color = "blue";
 double price = 5000.00;

 void drive(){
    System.out.println("You drive the car");
 }

 void brake(){
    System.out.println("You step on the brakes");
 }

 public String toString(){
    String myString = "("+make + "," + model +"," + color + "," + year+")";
    return myString;

 }
}
