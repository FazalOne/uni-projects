import java.util.ArrayList;

public class Hashmap {

    int count = 0; //No of categories in hashmap

    //Constructor for Hashmap
    public Hashmap(int initialSize) {hashTable =new Categories [initialSize];}

    Categories[] hashTable;
    //Hashmap is intended to be filled with unique Categories
    //Collisions are intended to be actual Business.
    //Collisions handled using separate chaining.

    public int hash(int key) {return key%hashTable.length;}

    public void resize () {
        if (count == hashTable.length) {  //for dynamic array
            Categories[] arr2 = new Categories[hashTable.length * 2];
            System.arraycopy(hashTable, 0, arr2, 0, hashTable.length);
            hashTable = arr2;
        }
    }

    //Inserting into Hashmap
    //No Collision Insert. O(1)
    public void put(ArrayList<Categories> category) {for (Categories Category:category){
        if (count == hashTable.length) this.resize();
        hashTable[hash(Category.getKey())] = Category;count++;}
    }

    //On category collision (i.e category already exists), separate chaining of Businesses.
    public void put(NodeBusiness business)
    {for (Categories Category:business.getCategory()) Category.getBusinessList().insertInOrder(business);}

    public Categories findCategory(String name){
        for (Categories category: hashTable)
        {if (category.getNameOfCategory().compareTo(name) == 0) return category;}
        return null;
    }

    public Categories[] getCategories(){return hashTable;}

    //delete functionality
    public void delete(int key, Categories category)
    {
        if(hashTable[hash(key)] == null) {return;}
        else hashTable[hash(key)].getBusinessList().clear();
    }

    public void delete(int key, String name)
    {
        if(hashTable[hash(key)] == null) {return;}
        else hashTable[hash(key)].getBusinessList().delete(name);
    }

    //returns the List of Businesses in a category
    public LinkedList find(Categories category) {return hashTable[hash(category.getKey())].getBusinessList();}

    //returns List of Businesses satisfying text query and specified category
    public ArrayList<NodeBusiness> find(Categories CatString, String NameString) {
        ArrayList<NodeBusiness> business = new ArrayList<>();
        //Categories Category = this.findCategory(CatString.getNameOfCategory());
        NodeBusiness temp = hashTable[hash(CatString.getKey())].getBusinessList().head;
        while(temp != null) {if(temp.getName().compareTo(NameString) == 0) business.add(temp);temp=temp.next;}
        if (business.isEmpty()) {System.out.println("Business not found");}
        return business;
    }

    //returns List of Businesses satisfying text query from all categories
    public ArrayList<NodeBusiness> search(String name)
    {
        ArrayList<NodeBusiness> business = new ArrayList<>();
        for (Categories categories : hashTable) {
            if (categories == null) continue;
            else {
                ArrayList<NodeBusiness> ResultsList = categories.getBusinessList().find(name);
                if (ResultsList != null) business.addAll(ResultsList);
            }
        }
        if(business.isEmpty()) return null;
        else return business;
    }

    //toString function to output the entire contents of Hashmap
    public String toString() {
        String str = "";
        for (Categories categories : hashTable) {
            if (categories == null) {continue;}
            else {str = str + "\n" + categories.getBusinessList().toString();}}
        return str;
    }
}

