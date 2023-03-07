//Ali Asghar Hussain 24525
//Syed Fazal Ul Hasan Mohani ERP 23024
//Tariq Iqbal 19091

import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        SearchEngine Demo = new SearchEngine(1);

        //defining categories of businesses
        ArrayList<Categories> SearchCategories = new ArrayList<>();
        String[] CategoryNames = {"alpha", "beta","gamma","omicron", "delta"};
        for (String CategoryName:CategoryNames)
        {
            Categories category = new Categories(CategoryName);
            SearchCategories.add(category);
        }
        Demo.insert(SearchCategories);

        //items of business
        Items item = new Items("stuff" , 2);
        Items item1 = new Items("placeholder" , 3);
        Items photographs = new Items("photographs" , 5);
        Items weddingCakes = new Items("cakes" , 1);
        Items venue = new Items("venue" , 4);

        //creating businesses
        NodeBusiness photography2 = new NodeBusiness("photographer", SearchCategories.get(0), item, 3.0);
        NodeBusiness photography = new NodeBusiness("photographer", SearchCategories.get(1), photographs, 2.0);
        NodeBusiness flowers = new NodeBusiness("flowers", SearchCategories.get(2), item1, 1.0);
        NodeBusiness test = new NodeBusiness("test", SearchCategories.get(3), item1, 5.0);
        NodeBusiness west = new NodeBusiness("west", SearchCategories.get(2), item1, 3.0);
        NodeBusiness cakes = new NodeBusiness("cakes", SearchCategories.get(1), weddingCakes, 5.0);
        NodeBusiness wedding = new NodeBusiness("wedding", SearchCategories.get(4), venue, 3.0);

        //adding businesses to search engine
        Demo.insert(photography);
        Demo.insert(test);
        Demo.insert(west);
        Demo.insert(photography2);
        Demo.insert(flowers);
        Demo.insert(cakes);
        Demo.insert(wedding);

        System.out.println();

        GUI gui = new GUI (Demo) ;
        gui.Display();

    }
}
