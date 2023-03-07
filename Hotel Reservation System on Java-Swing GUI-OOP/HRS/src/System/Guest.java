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
public class Guest implements Serializable {
    private String Name;
    private int CNIC;
    private int phoneNumber,creditCardNo;
    private String password, username;
    private ArrayList<Guest> list = this.getData();
    public ArrayList<Rooms> roomList; 
    public ArrayList<Amenities> aList;
    
    
     private ArrayList<Rooms> getUserRData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream(this.getName()+"R.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Rooms>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Rooms>();
        }
     }
     private ArrayList<Amenities> getUserAData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream(this.getName()+"A.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Amenities>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Amenities>();
        }
     }
        
    public Guest(){}
    
    public Guest(int n){
        this.Name = list.get(n).getName();
        this.CNIC = list.get(n).CNIC;
        this.phoneNumber = list.get(n).phoneNumber;
        this.creditCardNo = list.get(n).creditCardNo;
        this.username = list.get(n).username;
        this.password = list.get(n).password;
        this.roomList = list.get(n).getUserRData();
        this.aList = list.get(n).getUserAData();
    }
    
    public Guest(String name, int CNIC, int phoneNumber, int creditCardNo, String username, String password){
        this.Name = name;
        this.CNIC = CNIC;
        this.phoneNumber = phoneNumber;
        this.creditCardNo = creditCardNo;
        this.username = username;
        this.password = password;
        this.roomList = getUserRData();
        this.aList = getUserAData();
        list.add(this);
        this.writeFile();
    }
    
    private ArrayList<Guest> getData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream("GuestData.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Guest>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Guest>();
        }
        
    
}
    private void writeFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream("GuestData.dat"));
            o1.writeObject(list);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
     }
    
    private String getUsername(){
        return this.username;
        }
      private String getPassword(){
          return this.password;
      }
        
        public boolean checkID(String username, String password ){
            for (int i =0 ; i<list.size(); i++){
                if (list.get(i).getUsername().equals(username) && list.get(i).getPassword().equals(password))
                    return true;
            }
            return false;
        }
        
        public int getUserIDInt(String username, String password ){
            for (int i =0 ; i<list.size(); i++){
                if (list.get(i).getUsername().equals(username) && list.get(i).getPassword().equals(password))
                    return i;
            }
            return Integer.parseInt(null);
        }
        
        public Guest get(int n){
           return  list.get(n);
        }
        
        public String getName(){return Name;}
        
        public void addRoom(Rooms r){
        this.roomList.add(r);
        this.writeRoomFile();
        }
        
         public void writeRoomFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream(this.getName()+"R.dat"));
            o1.writeObject(roomList);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
     }
         public void addAmenities(Amenities r){
        this.aList.add(r);
        this.writeAmenitiesFile();
        }
           public void writeAmenitiesFile(){
      try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream(this.getName()+"A.dat"));
            o1.writeObject(aList);
            o1.close();
        } catch (IOException ex) {
            System.out.println(ex);
        }
     }
    
}
