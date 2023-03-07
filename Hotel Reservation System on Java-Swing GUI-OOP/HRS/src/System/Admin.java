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
public class Admin implements Serializable {
    private String Name;
    private int ID,CNIC;
    private int phoneNumber;
    private String password, username;
    private ArrayList<Admin> list = this.getData();
    
    public Admin(){}
    public Admin(String name, int id, int CNIC, int phoneNumber, String username ,String password){
       this.Name = name;
       ID =id;
       this.phoneNumber = phoneNumber;
       this.username = username;
       this.password = password;
       list.add(this);
        try {
            ObjectOutputStream o1 = new ObjectOutputStream(new FileOutputStream("AdminData.dat"));
            o1.writeObject(list);
        } catch (IOException ex) {
            System.out.println(ex);
        }
    }
    
    private ArrayList<Admin> getData(){
        try{
        ObjectInputStream o2 = new ObjectInputStream(new FileInputStream("AdminData.dat"));
        return (ArrayList)o2.readObject();
        }
        catch(IOException e ){
            return new ArrayList<Admin>();
        } catch (ClassNotFoundException ex) {
           return new ArrayList<Admin>();
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
    
}
