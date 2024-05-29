import java.util.Scanner;

public class switchCase{
    public static void main(String[] args){
        Scanner in = new Scanner(System.in);
        System.out.println("Enter a fruit of your choice.");
        String fruit = in.next();
        switch(fruit){
            case "Mango":
            System.out.println("King of fruits.");
            break;
            case "Apple":
            System.out.println("I like apple.");
            case "Orange":
            System.out.println("I don;t like orange.");
            default:
            System.out.println("I don't like anything.");
        }        
    }
}