import java.util.ArrayList;

public class NodeBusiness {
    public NodeBusiness next;
    private double priceRating; private int popularity; private String name;
    private ArrayList<Items> itemsList = new ArrayList<>(); private ArrayList<Categories> keyWordsList = new ArrayList<>();

    //constructors for NodeBusiness
    public NodeBusiness(String name, Categories Category, Items item, double Popularity)
    {
        this.name = name;
        addItem(item);
        addKeyWords(Category);
        calculatePriceRating();
        setPopularity(Popularity);
    }

    public NodeBusiness(String name, ArrayList<Categories> CategoryList, ArrayList<Items> itemList, double Popularity)
    {
        this.name = name;
        setItemsList(itemList);
        setKeyWords(CategoryList);
        calculatePriceRating();
        setPopularity(Popularity);
    }

    //name getters setters
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }

    //priceRating getters setters
    public void calculatePriceRating()
    {
        double priceRating = 0;
        for (Items items : itemsList) {
            priceRating = priceRating + items.getPrice();
        }
        priceRating = priceRating/itemsList.size();
        this.priceRating = priceRating;
    }
    public double getPriceRating() {
        return priceRating;
    }

    //item getters setters
    public void setItemsList(ArrayList<Items> itemsList) {
        this.itemsList = itemsList;
    }
    public void addItem(Items item) { this.itemsList.add(item); calculatePriceRating(); }
    public void removeItem(Items item) { this.itemsList.remove(item); calculatePriceRating(); }
    public ArrayList<Items> getItemsList() { return itemsList; }
    public String getItems() { return itemsList.toString(); } //used for printing items

    //keywords getters setters
    public void setKeyWords(ArrayList<Categories> keyWords) {
        this.keyWordsList = keyWords;
    }
    public void addKeyWords(Categories keyWord) { this.keyWordsList.add(keyWord); }
    public void removeCategory(Categories keyWord) { this.keyWordsList.remove(keyWord); }
    public ArrayList<Categories> getCategory() { return keyWordsList; } //used for search contains in LinkedList
    public String getKeyWords() { return keyWordsList.toString(); } //used for printing keywords in NodeBusiness, ResultsList

    //popularity getters setters
    public void setPopularity(double Popularity) {this.popularity = (int)(Popularity); }
    public String getPopularity() {
        int i = 0;
        String Stars = "";
        while (i < this.popularity) {Stars += "*"; i++;}
        return Stars;
    }

    //toString function to print details of business
    public String toString() {
        String s = "Business Name: ";
        String data = this.getName() + " | Category:" + this.getKeyWords() + " | $ " + this.getPriceRating() + " | Ranking " + this.getPopularity();
        String items = this.getItems();
        s += data + "\n" + "Items: "+ items.toString();
        return s + "\n--------------------------------------------------------\n";
    }
}
