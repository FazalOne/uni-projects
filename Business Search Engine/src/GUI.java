import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax . swing . JButton ;
import javax . swing . JFrame ;
import javax . swing . JLabel ;
import javax . swing . JPanel ;
import javax . swing . JTextField ;
import javax.swing.*;

public class GUI implements ActionListener {
    int count = 0;

    Categories[] searchCategory;

    private static JTextField searchVal_text;
    private static JTextField lastName_text;
    private static JTextField ID_text;
    private static JComboBox category;

    SearchEngine Demo;

    public GUI(SearchEngine searchEngine) {
        this.Demo = searchEngine;
    }

    //GUI frame
    public void Display() {
        JFrame frame = new JFrame(" Business Search Engine ");
        JPanel panel = new JPanel();
        frame.setSize(300, 225);
        frame.setLocation(600, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        panel.setLayout(null);
        String[] categories = getCategories();

        category = new JComboBox(categories);
        category.setBounds(100, 70, 150, 20);
        panel.add(category);
        panel.setLayout(null);
        panel.setSize(400, 500);
        panel.setVisible(true);

        JLabel searchVal = new JLabel("Search : ");
        JLabel category = new JLabel(" Category : ");

        searchVal.setBounds(10, 10, 150, 20);
        category.setBounds(6, 70, 150, 20);

        panel.add(searchVal);
        panel.add(category);

        searchVal_text = new JTextField();
        ID_text = new JTextField();

        searchVal_text.setBounds(100, 10, 150, 20);
        ID_text.setBounds(100, 50, 150, 20);

        panel.add(searchVal_text);

        JButton searchButton = new JButton(" Search ");
        searchButton.setBounds(100, 100, 150, 20);

        panel.add(searchButton);
        frame.setVisible(true);

        searchButton.addActionListener(new GUI(Demo));
    }

    //on Search button click
    public void actionPerformed(ActionEvent e) {

        String searchText = searchVal_text.getText();
        int catIndex = category.getSelectedIndex();
        setSearchCategory();
        String catText = category.getSelectedItem().toString();

        if (searchText.length() > 0) {
            if (catText.compareTo("All") == 0) {System.out.println(Demo.search(searchText));}
            else {System.out.println(Demo.search(searchCategory[catIndex-1], searchText));}
        }
        else if (catText.compareTo("All") == 0) {System.out.println(Demo.PrintHashmap());}
        else {
            System.out.println(Demo.search(searchCategory[catIndex-1]));
        }

    }

    public String[] getCategories() {  //displays existing categories in GUI dropdown menu
        Categories[] searchCategory1 = Demo.getCategory();
        searchCategory = searchCategory1;

        String[] CategoryString = new String[searchCategory1.length + 1];
        CategoryString[0] = "All";

        for (int i = 1; i < CategoryString.length; i++) {
            if (searchCategory1[i - 1] != null) CategoryString[i] = searchCategory1[i - 1].toString();
        }
        return CategoryString;
    }

    public void setSearchCategory(){
        Categories[] searchCategory1 = Demo.getCategory();
        searchCategory = searchCategory1;
    }
}