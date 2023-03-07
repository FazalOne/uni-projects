/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package System;
import java.io.*;
import java.util.ArrayList;

/**
 *
 * @author User
 */
public class Amenities implements Serializable {
    private String Type, Hotel;
    private int price;
    public ArrayList<Amenities> list = this.getData();
    
    public Amenities(){}
    public Amenities(String type, String hotel, int price){
        this.Type = type;
        this.Hotel = hotel;
        this.price = price;
        list.add(this);
        this.writeFile();
        
    }
    
    public String getType(){return Type;}
    public String getHotel(){return Hotel;}
    public int getPrice(){return price;}
    
     private ArrayList<Amenities> getData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream("AmenitiesData.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Amenities>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Amenities>();
        }
    }
     private void writeFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream("AmenitiesData.dat"));
            o1.writeObject(list);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
     }
      public void remove(int n){
     list.remove(n);
     this.writeFile();
     }
}
