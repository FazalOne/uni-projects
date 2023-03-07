//Ali Asghar Hussain 24525
//Syed Fazal Ul Hasan Mohani ERP 23024
//Tariq Iqbal 19091

import java.util.ArrayList;
public class SearchEngine {
    private Hashmap hash;

    public SearchEngine(int size)
    {
        hash = new Hashmap(size);
    }    //constructor for SearchEngine

    public String printSearch(NodeBusiness business)
    {
        int i = 0;
        String str = "";
        NodeBusiness temp = business;
        while(i<5 && temp != null)
        {
            str = str + temp.toString();
            temp = temp.next;
        }
        return str;
    }
    public Hashmap PrintHashmap(){
        return hash;
    }   //returns Hashmap so Hashmap toString can be called
    public Categories[] getCategory() {return hash.getCategories();} //returns categories of hashmaps (used to populate dropdown in GUI)

    public void delete(Categories category) {hash.delete(category.getKey(), category);} //possible future use

    public void delete(Categories category, String name) {hash.delete(category.getKey(), name);} //possible future use
    public void insert(ArrayList<Categories> category) {hash.put(category);} //inserts list of categories at compile time (initial categorylist)
    public void insert(NodeBusiness business) {hash.put(business);} //inserts business into hashmap.
    public LinkedList search(Categories category) {return hash.find(category);} //returns a complete category LinkedList containing all the businesses
    public ArrayList<NodeBusiness> search(Categories CatString, String name) {return hash.find(CatString, name);} //returns Businesses satisfying search in category
    public ArrayList<NodeBusiness> search(String name) {return hash.search(name);} //returns Businesses satisfying search in Hashmap
}
