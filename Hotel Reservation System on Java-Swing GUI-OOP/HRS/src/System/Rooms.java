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
public class Rooms implements Serializable {
    
    
    
    private String roomType, roomSize;
    private int roomNumber,price;
    private String occupied;
    private String hotelName;
    private String occupiedBy;
    public ArrayList<Rooms> list = this.getData();
    
    public Rooms(){}
    public Rooms(int roomNumber, String roomType, String roomSize, String occupied, String hotelName,int price){
        
    this.roomNumber = roomNumber;
    this.hotelName = hotelName;
    this.occupied = occupied;
    this.roomSize = roomSize;
    this.roomType = roomType;
    this.price =price;
    this.occupiedBy = null;
    
    list.add(this);
       this.writeFile();
    
    }
    
    public void  setOccupiedName(String name){
        this.occupiedBy = name;
        this.writeFile();
    }
    
    public String getOccupiedName(){
        return this.occupiedBy;
    }
    
    private ArrayList<Rooms> getData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream("RoomsData.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Rooms>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Rooms>();
        }
    }
    
     public int getRoomNumber(){return roomNumber;}
     public int getPrice(){return price;}
     public String getRoomType(){return roomType;}
     public String getRoomSize(){return roomSize;}
     public String IsRoomAvailable(){return occupied;}
     public String getHotelName(){return hotelName;}
     
     public void removeRoom(int n){
     list.remove(n);
     this.writeFile();
     }
     
     private void writeFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream("RoomsData.dat"));
            o1.writeObject(list);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
     }
     public void changeVacancy(){
     if(this.occupied.equals("YES"))
         this.occupied = "NO";
     else this.occupied = "YES";
     
     this.writeFile();
     }
}
