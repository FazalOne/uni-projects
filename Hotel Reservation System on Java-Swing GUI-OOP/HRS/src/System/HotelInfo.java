/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package System;
import java.util.ArrayList;
import java.io.*;

/**
 *
 * @author User
 */
public class HotelInfo implements Serializable {
    private String Name, Address, typeOfHotel, website;
    private int phoneNo, rating;
    public ArrayList<HotelInfo> list = getData();
    
    public HotelInfo(){}
    
    public HotelInfo(String Name, String Address, String typeOfHotel, String website, int phoneNo, int rating){
        this.Name = Name;
        this.Address = Address;
        this.typeOfHotel = typeOfHotel;
        this.website = website;
        this.phoneNo  = phoneNo;
        this.rating = rating;
        
        list.add(this);
        this.writeFile();
    }
    private ArrayList<HotelInfo> getData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream("HotelInfo.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<HotelInfo>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<HotelInfo>();
        }
    }
    private void writeFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream("HotelInfo.dat"));
            o1.writeObject(list);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
        
     }
    
    public String getName(){return this.Name;}
    
    public String getHotelInfo(){return String.format("Name: %s\nAddress: %s\nWebsite: %s\n"
            + "Type of Hotel: %s\nPhone Number: %s\nRating: %s\n",Name,Address,website,typeOfHotel,phoneNo,rating);
            }
}
