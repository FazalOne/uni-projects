public class Categories { //Categories populate the hashmap

    Categories(String name){
        setNameOfCategory(name);
        key = count++;
        businessList = new LinkedList();
    }
    private String nameOfCategory;
    private static int count = 0;
    int key;
    private LinkedList businessList;
    public int getKey() {
        return key;
    }
    public LinkedList getBusinessList() {
        return businessList;
    }
    public String getNameOfCategory() {return nameOfCategory;}
    public void setNameOfCategory(String nameOfCategory) {this.nameOfCategory = nameOfCategory.toLowerCase();}

    @Override
    public String toString() {
        return nameOfCategory;
    }
}
