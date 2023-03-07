import org.w3c.dom.Node;

import java.lang.reflect.Array;
import java.sql.ResultSet;
import java.util.ArrayList;

public class LinkedList {
    NodeBusiness head;
    public boolean isEmpty() {if (head == null) return true; else return false;}

    public void insertInOrder(String name, Categories category, Items item, double popularity) {
        NodeBusiness newNode = new NodeBusiness(name, category, item, popularity);
        insertInOrder(newNode);
    }
    public void insertInOrder(NodeBusiness newNode) {
        if (isEmpty()) {head = newNode;}
        else {
            NodeBusiness temp = head; NodeBusiness prev = head;
            while (temp.next != null && temp.getPriceRating() > newNode.getPriceRating()) {prev = temp;temp = temp.next;}
            if (temp == head) {newNode.next = head;head = newNode;}
            else if (temp.next == null) {temp.next = newNode;}
            else {newNode.next = temp;prev.next = newNode;}
        }
    }

    public void delete(String name) {
        if (isEmpty()) {return;}
        else {
            NodeBusiness temp = head; NodeBusiness prev = head;
            while (temp != null && temp.getName().compareTo(name) != 0) {prev = temp;temp = temp.next;}
            if(temp == head) {head = temp.next; temp.next = null;}
            else if(temp == null) {System.out.println("Business not found");}
            else {prev.next = temp.next;}
        }
    }
    public void clear() {head = null;}
    public ArrayList<NodeBusiness> find(String name) {
        ArrayList<NodeBusiness> ResultsList = new ArrayList<>();
        NodeBusiness temp = head;
        while(temp != null) {
            if(temp.getName().compareTo(name) == 0) {ResultsList.add(temp);}
            temp=temp.next;}
        return ResultsList;
    }

    @Override
    public String toString() {
        String str = "";
        NodeBusiness temp = head;
        while(temp != null)
        {
            str = str + temp;
            temp = temp.next;
        }
        return str;
    }
}
