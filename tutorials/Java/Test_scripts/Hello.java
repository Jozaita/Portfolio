/*
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Random;
import java.util.Scanner;

import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JLayeredPane;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.border.Border;
import javax.sound.sampled.*;

import Package2.C;
*/

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.ObjectStreamClass;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Timer;
import java.util.TimerTask;

enum Planet {

    MERCURY(1),
    VENUS(2),
    EARTH(3),
    MARS(4),
    JUPITER(5),
    SATURN(6),
    URANUS(7),
    NEPTUNE(8),
    PLUTO(9);

    int number;
    Planet(int num){
        this.number = num;
    }
}

public class Hello {

    public static void main(String[] args) throws IOException, ClassNotFoundException {
        /*
        System.out.print("Hello World!\n");
        System.out.println("I am here in Java!");
        System.out.println("\t tabulando!");
        System.out.print("\" By Juan!\"");
        


        String name = "juan";
        System.out.println("Hello " + name);
        
        


        int x = 123;
        System.out.println(x);

        long p = 12312312312312312L;
        System.out.println(p);

        char y; 
        y = 'y';
        System.out.println(y);

        float q = 123.34f;
        System.out.println(q);

        //Also double,short, byte and String (with capital because it is reference, not primitive)

        // This is a comment 
        /* Just
            * like in regular javascript
        

            String x = "water";
            String y = "koolaid";
            String temp;
            System.out.println("X:"+x);
            System.out.println("Y:"+y);

            temp = x;
            x = y;
            y= temp;

            System.out.println("X:"+x);
            System.out.println("Y:"+y);
            
        Scanner scanner = new Scanner(System.in);

        System.out.println("What is your name");
        String name = scanner.nextLine();
        System.out.println("How old are you?");
        int age = scanner.nextInt();
        //Si se llama un nextLine despues de un nextInt, hay problemas por la secuencia de escape, se salta la respuesta
        // Se debe limpiar el scanner con otra nueva línea no asignada (scanner.nextLine())

        System.out.println("Hello "+name);
        System.out.println("You are "+age+" years old");
        
        //Expressions and operators
        double friends = 10;
        friends += 1;
        friends++;
        friends = (double) friends/5;
        System.out.println(friends);

        
        

        //GUI program introduction
        String name = JOptionPane.showInputDialog("Enter your name:");
        JOptionPane.showMessageDialog(null, "Hello "+name);

        int age =Integer.parseInt(JOptionPane.showInputDialog("Enter your age: "));
        JOptionPane.showMessageDialog(null, "You are "+age+" years old");

        double
        height =Double.parseDouble(JOptionPane.showInputDialog("Enter your height: "));
        JOptionPane.showMessageDialog(null, "You are "+height +" cm tall");   
       

        //Math class

        double x = 3.14;
        double y = -10;

        double c = Math.max(x,y);
        double c_1 = Math.abs(y);
        // Math.sqrt,math.round,math.ceil,math.floor

        System.out.println(c);
        System.out.println(c_1);

        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter side x:");
        x =scanner.nextDouble();
        System.out.println("Enter side y");
        y =scanner.nextDouble();
        c = Math.sqrt(x*x + y*y);
        System.out.println("The hypothenuse is " + c);
        scanner.close();
        
      

         //Random numbers

        Random random = new Random();

        //int x = random.nextInt(6)+1;
        //double x = random.nextDouble();
        boolean x = random.nextBoolean();

        System.out.println(x);

        int age = 22;
        if (age==18){
            System.out.println("You just turned 18!");
        }else if(age<18){
                System.out.println("Keep growing");
            }else{
                System.out.println("OK boomer");
            };

      

        // Switch class

        String day = "zz<<";
        switch(day){
            case "Sunday": System.out.println("It is sunday");
            break; //if not break, prints below until break
            case "Monday": System.out.println("It is monday");
            break;
            case "Tuesday": System.out.println("It is tuesday");
            break;
            case "Wednesday": System.out.println("It is wednesday");
            break;
            default: System.out.println("Another day");
                    }
        

        // Logical operators class
        int temp = 25;
        if (temp>30){
            System.out.println("It is hot!");
        }else if (temp>=20 && temp<=30){
            System.out.println("It is warm");
        }else{
            System.out.println("It is cold");
        }

        Scanner scanner = new Scanner(System.in);
        System.out.println("Wanna quit? (press q)?");
        String response = scanner.next(); //next work for keys
        if (response.equals("q") || response.equals("Q")){ // for string the method equalsq
            System.out.println("Quit the game! ");
        };


        // While loop 
        Scanner scanner = new Scanner(System.in);
        String name = "";

        while (name.isBlank()){
            System.out.print("Enter your name: ");
            name = scanner.nextLine();
        }

        System.out.println("Hello " + name);
        
        do{
            System.out.print("Enter your name: ");
            name = scanner.nextLine();
        }while (name.isBlank());

        System.out.println("Hello " + name);
        

        // For loop

        for (int i = 0;i<=10;i++){
            System.out.println(i);
            // The third parameter, incremental, can be moved to the end of the for loop
        };

        

        //Nested loops

        Scanner scanner = new Scanner(System.in);

        int rows;
        int columns;
        String symbol = "";

        System.out.println("Enter # of rows: ");
        rows = scanner.nextInt();
        System.out.println("Enter # of columns");
        columns = scanner.nextInt();
        System.out.println("Enter symbol to use: ");
        symbol = scanner.next();

        for (int i=1;i<=rows;i++){
            System.out.println();
            for (int j=1;j<=columns;j++){
                System.out.print(symbol);

            }
        
        }
        

        // Arrays

        String[] cars = {"Camaro","Corvette","Tesla"};
        String[] brands = new String[3];
        // All arrays need to have the same datatype

        brands[0] = "Nestle";
        brands[1] = "Apple";
        //Not all the values need to be assigned, but allocated

        System.out.println(cars[0]);

        cars[0] = "Mustang";

        System.out.println(cars[0]);

        for (int i=0;i<cars.length;i++){
            System.out.println(cars[i]);
        }
        

        // 2D arrays

        String [][] cars = new String[3][3];
        String [][] numbers = {{"1","2","3"},{"1","2","3"},{"1","2","3"}};

        cars[0][0] = "Camaro";
        cars[0][1] = "Tesla";
        cars[0][2] = "Corvette";
        cars[1][0] = "Camaro";
        cars[1][1] = "Tesla";
        cars[1][2] = "Corvette";
        cars[2][0] = "Camaro";
        cars[2][1] = "Tesla";
        cars[2][2] = "Corvette";


        for (int i=0;i<cars.length;i++){
            System.out.println("");
            for (int j=0;j<cars[i].length;j++){
                System.out.print(cars[i][j]+ " ");
            }
        }
        for (int i=0;i<numbers.length;i++){
        System.out.println("");
        for (int j=0;j<numbers[i].length;j++){
            System.out.print(numbers[i][j]+ " ");
        }
    }
    

    // String methods 
    String name = "juan";

    //boolean result = name.equals("juan");
    //boolean result = name.equalsIgnoreCase("JuaN");
    //int result = name.length();
    //char result = name.charAt(0);
    //int result = name.indexOf("j");
    //boolean result = name.isEmpty();
    //String result = name.toUpperCase();
    //String result = name.toLowerCase();
    //String result = name.trim();
    String result = name.replace("u","o");


    System.out.println(result);
    

    // Wrapper classes
    // The primitive datatypes have its counterpart in Datatypes with an uppercase
    // boolean vs Boolean, the corresponding reference datatype. 
    // There is automatic conversion implemented between the two (unboxing vs autoboxing)
    
    Boolean a = true;
    Character b = '#';
    // Using the reference datatypes have the advantage of the implemented methods
    // Can be used in certain collections

    if (a == true){
        System.out.println("This is true");
    }
   

    // ArrayList

    ArrayList<String> food = new ArrayList();
    food.add("Rice");
    food.add("Pizza");
    food.add("Salad");
    //ArrayList<Integer> Use Wrapper

    food.set(0,"sushi");
    food.remove("Salad"); //Also work with interger
    food.clear();


    for (int i=0;i<food.size();i++){
        System.out.println(food.get(i));
    }
     

    // 2D ArrayList

    ArrayList<ArrayList<String>> groceryList = new ArrayList();

    ArrayList<String> bakeryList = new ArrayList<String>();
    bakeryList.add("pasta");
    bakeryList.add("garlic bread");
    bakeryList.add("donuts");

    ArrayList<String> produceList = new ArrayList<String>();
    produceList.add("tomatoes");
    produceList.add("zucchini");
    produceList.add("peppers");

    ArrayList<String> drinksList = new ArrayList<String>();
    drinksList.add("soda");
    drinksList.add("coffee");

    groceryList.add(bakeryList);
    groceryList.add(produceList);
    groceryList.add(drinksList);


    System.out.println(groceryList.get(0));
    

    // For-each loop

    //String[] animals = {"cat","dog","rat","bird"};
    ArrayList<String> animals = new ArrayList<String>();
    animals.add("cat");
    animals.add("dog");
    animals.add("rat");
    animals.add("bird");

    for (String i : animals){
        System.out.println(i);
    }
    


    //String name = "Juan";
    //int age = 14;
    //main(name,age);

    int x = 3;
    int y = 4;

    System.out.println(add(x,y));
    

    //Overloaded methods
    // They have the same name but different arguments
    double x = add(2.4,2.4,1.2);
    System.out.println(x);
    

    //Printf method

    

    boolean myBoolean = true;
    char myChar = '@';
    String myString = "Bro";
    int myInt = 50;
    double myDouble = 1000;

    //System.out.printf("This is a format string %b",myBoolean);
    //System.out.printf("This is a format string %c",myChar);
    //System.out.printf("This is a format string %10s",myString);
    //System.out.printf("This is a format string %d",myInt);
    //System.out.printf("This is a format string %10.2f",myDouble);
    

    // Final keyword
    final double PI = 3.141592654;

    //PI = 4; FORBIDDEN !

    System.out.println(PI);
    

    Car myCar1 = new Car();
    Car myCar2 = new Car();

    System.out.println(myCar1.model);
    System.out.println(myCar1.make);

    myCar1.brake();
    myCar1.drive();

    System.out.println(myCar2.model);
    System.out.println(myCar2.make);
    

    //Constructors

    Human human = new Human("Juan",29,87.8);
    Human human2 = new Human("Carolina",33,50.1);

    System.out.println(human.name);
    System.out.println(human2.name);

    human2.eat();
    human.drink();

    
    //Overloaded constructors
    Pizza pizza = new Pizza("Chapata","BBQ","Mozza");
    System.out.println(pizza.bread);
    System.out.println(pizza.sauce);
    System.out.println(pizza.cheese);
    System.out.println(pizza.topping);
    

    //toString method
    Car car = new Car();
    System.out.println(car);
    System.out.println(car.toString());
    
    //Array of objects 
    int [] numbers = new int[3];
    char[] characters = new char[4];
    String[] names = new String[5];
    //Food[] refrigerator = new Food[3];

    Food food1 = new Food("pizza");
    Food food2 = new Food("hotdog");
    Food food3 = new Food("rice");

    Food[] refrigerator = {food1,food2,food3};

    //refrigerator[0] = food1;
    //refrigerator[1] = food2;
    //refrigerator[2] = food3;

    System.out.println(refrigerator[1]);
    

    Garage garage = new Garage();
    Car2 car = new Car2("BMW");
    Car2 car2 = new Car2("SEAT");
    garage.park(car);
    garage.park(car2);
    

    // The static keyword
    Friend friend1 = new Friend("Alice");
    Friend friend2 = new Friend("Bob");
    Friend friend3 = new Friend("Bob2");

    System.out.println(Friend.numberOfFriends);
    System.out.println(friend1.numberOfFriends);
    Friend.displayFriends();
    

    // Inheritance

    Car3 car = new Car3();
    Bycicle bike = new Bycicle();

    car.go();
    bike.stop();

    System.out.println(car.doors);
    System.out.println(bike.pedals);
    

    // Method overriding

    Dog dog = new Dog();
    dog.speak();

    

    // The super keyword

    Hero hero1 = new Hero("Batman",76,"Money");

    System.out.println(hero1.age);
    System.out.println(hero1.name);
    System.out.println(hero1.power);

    Hero hero2 = new Hero("Superman",87,"Laundry");

    System.out.println(hero1);

   

    // abstraction
    // abstract classes can not be instatiated, but subclasses can
    Car3 car = new Car3();
    //Vehicle veh = new Vehicle();
    
    
    //Access modifiers
    //check packages 
    

    // Encapsulation
    Car4 car = new Car4("Chevrolet", "Camaro", 1990);
    System.out.println(car.getMake());

    car.setYear(2022);
    System.out.println(car.getYear());

    

    //Copying objects
    Car4 car1 = new Car4("Chevrolet", "Camaro", 2021);
    //Car4 car2 = new Car4("Ford", "Mustang", 2022);
    //car2.copy(car1);
    Car4 car2 = new Car4(car1);

    System.out.println(car1);
    System.out.println(car2);
    System.out.println();
    System.out.println(car1.getMake());
    System.out.println(car1.getModel());
    System.out.println(car1.getYear());
    System.out.println(car2.getMake());
    System.out.println(car2.getModel());
    System.out.println(car2.getYear());
   

    //Interfaces 
    Rabbit rabbit = new Rabbit();
    rabbit.flee(); 
    Hawk hawk = new Hawk();
    hawk.hunt();
    Fish fish = new Fish();
    fish.flee();
    fish.hunt();

    //Polymorphism
    Bycicle bike = new Bycicle();
    Car3 car = new Car3();

    Vehicle[] racers = {car,bike};

    for(Vehicle x: racers){
        x.greet();
    }
    

    Animal animal;

    Scanner scanner = new Scanner(System.in);
    System.out.println("Which animal do you want?1=dog/2=cat");
    int response = scanner.nextInt();

    if (response == 1){
        animal = new Dog();

    } else if (response == 2){
        animal = new Cat();

    }else {
        animal = new Animal();
        
    }
    animal.speak();
    

    // Exception handling

    Scanner scanner = new Scanner(System.in);
    try{ 
        
        System.out.println("Enter a whole number to divide: ");
        int x= scanner.nextInt();
        System.out.println("Enter a whole number to divide by: ");
        int y = scanner.nextInt();

        int z = x/y;

        System.out.println("result: "+z);} 
        
        catch(ArithmeticException e){
            System.out.println("Can not divide by zero");
        }
        catch(InputMismatchException e){
            System.out.println("please, enter a number");
        }
        finally {System.out.println("This text will be displayed");
                 scanner.close();}

    

    //File class

    File file = new File("secret_message.txt");

    if (file.exists()){
        System.out.println("That file exists!");
        System.out.println(file.getPath());
        System.out.println(file.getAbsolutePath());
        System.out.println(file.isFile());
        //file.delete();
    } else { 
        System.out.println("The file does not exist");
    }

    

    //File writer
    try{
        FileWriter writer = new FileWriter("poem.txt");
        writer.write("Roses are red\n Violets are blue \n");
        writer.append("Como va la cosilla");
        writer.close();
    } catch (IOException e){
        e.printStackTrace();
    }
    

    //File reader
    try {
        FileReader reader = new FileReader("poem.txt");
        int data = reader.read();
        while (data!=-1){
            System.out.println((char)data);
            data = reader.read();
        }
        reader.close();
    } catch (FileNotFoundException e){
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }
    

    //Audio
    File file = new File("test.wav");
    try {
        Scanner scanner = new Scanner(System.in);
        AudioInputStream audiostream = AudioSystem.getAudioInputStream(file);
        Clip clip = AudioSystem.getClip();
        clip.open(audiostream);
        String response = "";
        while (!response.equals("Q")){
            System.out.println("P -> play, S -> STOP, R->RESET.Q->QUIT");
            System.out.println("Enter your choice");
            response = scanner.next();
            response = response.toUpperCase();
            switch(response){
                case "P": clip.start();
                break;
                case "S": clip.stop();
                break;
                case "R": clip.setMicrosecondPosition(0);
                break;
                case "Q": clip.close();
                break;
                default: System.out.println("Not a valid response");
            }
        }
        
    } catch (UnsupportedAudioFileException | IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    } catch (LineUnavailableException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }
    

    //Simple GUI

   
    JFrame frame = new JFrame(); 
    frame.setTitle("JFRAME TITLE GOES HERE");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setResizable(false);
    frame.setSize(420, 420);
    frame.setVisible(true);
    ImageIcon image = new ImageIcon("sombrero_azul.png");
    frame.setIconImage(image.getImage());
    //frame.getContentPane().setBackground(Color.GRAY);
    frame.getContentPane().setBackground(new Color(0,0,100));
    
    MyFrame myFrame = new MyFrame(); //Assignation not needed 

    
    // Labels

    ImageIcon image = new ImageIcon("sombrero_azul.png");
    Border border = BorderFactory.createLineBorder(Color.green,3);
    JLabel label = new JLabel();
    label.setText("Good morning! ");
    label.setIcon(image);
    label.setHorizontalTextPosition(JLabel.CENTER);
    label.setVerticalTextPosition(JLabel.TOP);
    label.setForeground(Color.DARK_GRAY);
    label.setFont(new Font("MV Boli",Font.BOLD,20));
    label.setIconTextGap(10);
    label.setBackground(Color.RED);
    label.setOpaque(true );
    label.setBorder(border);
    label.setVerticalAlignment(JLabel.CENTER);
    label.setHorizontalAlignment(JLabel.CENTER);
    //label.setBounds(100, 0, 210, 210);


    MyFrame myFrame = new MyFrame();
    myFrame.add(label);
    myFrame.pack();
    //myFrame.setLayout(null);
    

    // Panels

    ImageIcon icon = new ImageIcon("sombrero_azul.png");


    JLabel label = new JLabel();
    label.setText("Hi");
    label.setIcon(icon);
    label.setVerticalAlignment(JLabel.TOP);
    label.setHorizontalAlignment(JLabel.CENTER);
    label.setBounds(0, 0, 75, 75);

    JPanel redPanel = new JPanel();
    JPanel bluePanel = new JPanel();
    JPanel greenPanel = new JPanel();
    redPanel.setBackground(Color.RED);
    redPanel.setBounds(0, 0, 250, 250);
    bluePanel.setBackground(Color.BLUE);
    bluePanel.setBounds(250, 0, 250, 250);
    greenPanel.setBackground(Color.GREEN);
    greenPanel.setBounds(0,250,500,250);
    greenPanel.setLayout(new BorderLayout());
    redPanel.setLayout(null);

    JFrame frame = new JFrame();
  
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setLayout(null);
    frame.setSize(750,750);
    frame.setVisible(true);
    greenPanel.add(label);
    redPanel.add(label);
    frame.add(redPanel);
    frame.add(bluePanel);
    frame.add(greenPanel);
    

    //Buttons

    new MyFrame2();

    

    //Border layout managers

    JFrame frame = new JFrame();
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(500, 500);
    frame.setLayout(new BorderLayout(10,10));
    frame.setVisible(true);

    JPanel panel1 = new JPanel();
    JPanel panel2 = new JPanel();
    JPanel panel3 = new JPanel();
    JPanel panel4 = new JPanel();
    JPanel panel5 = new JPanel();

    panel1.setBackground(Color.red);
    panel2.setBackground(Color.green);
    panel3.setBackground(Color.yellow);
    panel4.setBackground(Color.magenta);
    panel5.setBackground(Color.blue);

    panel1.setPreferredSize(new Dimension(100,100));
    panel2.setPreferredSize(new Dimension(100,100));
    panel3.setPreferredSize(new Dimension(100,100));
    panel4.setPreferredSize(new Dimension(100,100));
    panel5.setPreferredSize(new Dimension(100,100));

    //---- subpanels

    JPanel panel6 = new JPanel();
    JPanel panel7 = new JPanel();
    JPanel panel8 = new JPanel();
    JPanel panel9 = new JPanel();
    JPanel panel10 = new JPanel();

    panel6.setBackground(Color.red);
    panel7.setBackground(Color.green);
    panel8.setBackground(Color.yellow);
    panel9.setBackground(Color.magenta);
    panel10.setBackground(Color.blue);
    
    panel5.setLayout(new BorderLayout());

    panel6.setPreferredSize(new Dimension(100,100));
    panel7.setPreferredSize(new Dimension(100,100));
    panel8.setPreferredSize(new Dimension(100,100));
    panel9.setPreferredSize(new Dimension(100,100));
    panel10.setPreferredSize(new Dimension(100,100));

    panel5.add(panel6,BorderLayout.NORTH);
    panel5.add(panel7,BorderLayout.SOUTH);
    panel5.add(panel8,BorderLayout.WEST);
    panel5.add(panel9,BorderLayout.EAST);
    panel5.add(panel10,BorderLayout.CENTER);


    frame.add(panel1,BorderLayout.NORTH);
    frame.add(panel2,BorderLayout.WEST);
    frame.add(panel3,BorderLayout.EAST);
    frame.add(panel4,BorderLayout.SOUTH);
    frame.add(panel5,BorderLayout.CENTER);

    

    //Flow Layout manager

    JFrame frame = new JFrame();
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(500, 500);
    frame.setLayout(new FlowLayout(FlowLayout.CENTER,10,10));

    JPanel panel1 = new JPanel();
    panel1.setPreferredSize(new Dimension(250, 250));
    panel1.setBackground(Color.lightGray);
    panel1.setLayout(new FlowLayout());

    panel1.add(new JButton("1"));
    panel1.add(new JButton("2"));
    panel1.add(new JButton("3"));
    panel1.add(new JButton("4"));
    panel1.add(new JButton("5"));
    panel1.add(new JButton("6"));
    panel1.add(new JButton("7"));
    panel1.add(new JButton("8"));
    panel1.add(new JButton("9"));

    frame.add(panel1);


    frame.setVisible(true);
    

    // Grid Layout

    JFrame frame = new JFrame();
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(500, 500);
    frame.setLayout(new GridLayout(3,3,10,10));

    frame.add(new JButton("1"));
    frame.add(new JButton("2"));
    frame.add(new JButton("3"));
    frame.add(new JButton("4"));
    frame.add(new JButton("5"));
    frame.add(new JButton("6"));
    frame.add(new JButton("7"));
    frame.add(new JButton("8"));
    frame.add(new JButton("9"));
    frame.add(new JButton("10"));
    

    frame.setVisible(true);
    

    // Layered panes

    JLabel label1 = new JLabel();
    label1.setOpaque(true);
    label1.setBackground(Color.red);
    label1.setBounds(50,50,200,200);

    JLabel label2 = new JLabel();
    label2.setOpaque(true);
    label2.setBackground(Color.green);
    label2.setBounds(100,100,200,200);

    JLabel label3 = new JLabel();
    label3.setOpaque(true);
    label3.setBackground(Color.blue);
    label3.setBounds(150,150,200,200);

    JLayeredPane layeredPane = new JLayeredPane();
    layeredPane.setBounds(0,0,500,500);

   // layeredPane.add(label1,JLayeredPane.DEFAULT_LAYER);
   // layeredPane.add(label2,JLayeredPane.DEFAULT_LAYER);
   // layeredPane.add(label3,JLayeredPane.DRAG_LAYER);

    layeredPane.add(label1,Integer.valueOf(0));
    layeredPane.add(label2,Integer.valueOf(2));
    layeredPane.add(label3,Integer.valueOf(1));

    JFrame frame = new JFrame("JLayeredPane");
    frame.add(layeredPane); 
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(500, 500);
    frame.setLayout(null);
    frame.setVisible(true);
    

    // Open GUI window
    LaunchPage launchPage = new LaunchPage();

    
    //Dialog boxes 
    //JOptionPane.showMessageDialog(null, "Welcome!", "Title", JOptionPane.PLAIN_MESSAGE);
    //JOptionPane.showMessageDialog(null, "Welcome!", "Title", JOptionPane.INFORMATION_MESSAGE);
    //JOptionPane.showMessageDialog(null, "Welcome!", "Title", JOptionPane.QUESTION_MESSAGE);
    //JOptionPane.showMessageDialog(null, "Welcome!", "Title", JOptionPane.WARNING_MESSAGE);
    //JOptionPane.showMessageDialog(null, "Welcome!", "Title", JOptionPane.ERROR_MESSAGE);
    //int answer =JOptionPane.showConfirmDialog(null, "Confirm plz!", "Title", JOptionPane.YES_NO_CANCEL_OPTION);
    //System.out.println(answer);
    //String name = JOptionPane.showInputDialog(null, "What is your name?","Title");
    //System.out.println(name);
    //JOptionPane.showOptionDialog(null, "You are awesome!", "secret message",JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.INFORMATION_MESSAGE,null,null,null);
    String[] responses = {"Makinote","Queice","suuu"};
    JOptionPane.showOptionDialog(null, "You are awesome!", "secret message",JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.INFORMATION_MESSAGE,null,responses,null);
    

    //textField

    MyFrame frame = new MyFrame();
    

    //Check buttons

    new MyFrame3();
    

    // Radio buttons
    new MyFrame4();

   

    // Combo box

    new MyFrame5();
    

    // Sliders
    new SliderDemo();
    

    // Progress bar
    new ProgressBarDemo();
    

    //Menu bar
    new MyFrame6();
    

    //JFileChooser

    new MyFrame7();
    

    //Color chooser

    new MyFrame8();
    

    //Key listener

    new MyFrame9();

    

    //Mouse Listener

    new MyFrame10();

   

    // Drag and drop

    MyFrame11 myFrame = new MyFrame11();

      

     // Key Bindings

     Game game = new Game();

    

    // 2D Graphics y animarions me las salto 

    // Generics in JAVA
    // Only works in 1.5+

    Integer[] intArray = {1,2,3,4,5};
    Double[] doubleArray = {1.2,2.3,3.4,4.5,5.6};
    Character[] charArray = {'A','E','I','O','U'};
    String[] stringArray = {"My","name","is","juan","hello"};

    // In order to avoid creating different methods for diff dtypes
    public static <T> void display(T[] array){
        for (Thing x: array){
            System.out.println(x+" ");
        }
        System.out.println();
    } 

    display(intArray);

    public static <T> Thing getFirst(T[] array){
        return array[0]
    }

    getFirst(intArray);
    

    // Generic classes 

    //MyIntegerClass myInt = new MyIntegerClass(1);
    //MyDoubleClass myDouble = new MyDoubleClass(3.14);

    MyGenericClass<Integer,Integer> myInt = new MyGenericClass<>(1,2);
    MyGenericClass<Double,Double> myDouble = new MyGenericClass<>(3.14,1.2);
    //Recall
    ArrayList<String> myFriends = new ArrayList<>();
  
    System.out.println(myInt.getValue());
    System.out.println(myDouble.getValue());
    

    // Bounded types
    // Control the dtype that can be passed to generic functions
    // In the class definition, <Thing extends Number>
    

    // Serialization 

    User user = new User();

    user.name = "bro";
    user.password = "pizza";

    try {
        FileOutputStream fileOut = new FileOutputStream("UserInfo.ser");
        ObjectOutputStream out = new ObjectOutputStream(fileOut);
        out.writeObject(user);
        fileOut.close();
        out.close();

        System.out.println("Object Info Saved");
        long serialVersionuID = ObjectStreamClass.lookup(user.getClass()).getSerialVersionUID();
        System.out.println(serialVersionuID);
    } catch (FileNotFoundException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }

    User newUser;
    
    FileInputStream fileIn = new FileInputStream("UserInfo.ser");
    ObjectInputStream in = new ObjectInputStream(fileIn);
    newUser = (User) in.readObject();
    in.close();
    fileIn.close();
    System.out.println(newUser.name);
    System.out.println(newUser.password);

    

    // Timer tasks

    Timer timer = new Timer();

    TimerTask task = new TimerTask() {

        int counter = 10;
        @Override
        public void run() {
            if(counter>0){
                System.out.println(counter+" seconds");
                counter--;
            }else{
                System.out.println("HAPPY NEW YEAR!");
                timer.cancel();
            }
        }
    };
    
    //timer.schedule(task,2000);

    Calendar date = Calendar.getInstance();

    date.set(Calendar.YEAR,2020);
    date.set(Calendar.MONTH,Calendar.JUNE);
    date.set(Calendar.DAY_OF_MONTH,20);
    date.set(Calendar.HOUR_OF_DAY,0);
    date.set(Calendar.MINUTE,0);
    date.set(Calendar.SECOND,0);

    //timer.schedule(task,date.getTime());

    timer.scheduleAtFixedRate(task, 0, 1000);
    //timer.scheduleAtFixedRate(task, date.getTime(), 1000);
    
   
    
    // Threads

    System.out.println("Hello world!");
     

    // Method Chaining 

    String name = "bro";

    name = name.concat(" code").toUpperCase();

    System.out.println(name);
    

    // Enums in Java

    Planet myPlanet = Planet.EARTH;




    canILiveHere(Planet.EARTH);


    }

    static void  canILiveHere(Planet planet){
        switch(planet){
            case EARTH: System.out.println(planet.number);
            break;
            default: System.out.println(planet.number);
            break;
        }
    

    

    //Hash maps
    HashMap<String,String> countries = new HashMap<String,String>();

    // add a key and value 
    countries.put("USA","Washington DC");
    countries.put("France","Paris");
    countries.put("India","New Delhi");
    countries.put("Russia","Moscow");

    countries.remove("Russia");
    System.out.println(countries.get("France"));
    System.out.println(countries);
    System.out.println(countries.size());
    //countries.clear();
    countries.replace("USA","Detroit");
    System.out.println(countries.containsKey("England"));
    System.out.println(countries);

    for(String i: countries.values()){
        System.out.println(i);
    }

    

    // Custom exceptions 
    
    Scanner scan = new Scanner(System.in);
    System.out.println("Enter your age: ");
    int age = scan.nextInt();

    try{
        checkAge(age);
    }catch (Exception e){
        System.out.println("A problem occurred: " +e);
    }

    //System.out.println(countries);


    }

    private static void checkAge(int age) throws AgeException {
        if (age<18){
            throw new AgeException("aka b beas");
        }

    */



    };

    /* 
    static int add(int a, int b, int c){
        System.out.println("Overloaded method 3 values");
        return a+b+c;
    }

    static int add(int x,int y){
        System.out.println("Overloaded method 2 values");
        int z = x+y;
        return z;

    }

    static double add(double a, double b, double c){
        System.out.println("Overloaded method 3 doubles");
        return a+b+c;
    }

    static double add(double x,double y){
        System.out.println("Overloaded method 2 doubles");
        double z = x+y;
        return z;

    }

    static void main(String name, int age ){
        System.out.println("Main by "+name+", you seem "+age);
    }
    */    

}