public class Items {

    private String name;
    private double price;
    public double getPrice() {
        return price;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPrice(double price) {
        this.price = price;
    }
    public Items(String name, double price)
    {
        this.name = name;
        this.price = price;
    }

    @Override
    public String toString() {
        return this.name;
    }
}
