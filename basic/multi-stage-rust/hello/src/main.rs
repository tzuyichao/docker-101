fn main() {
    println!("Hello, world!");
    let my_list = [ "One", "Two", "Three" ];
    for num in &my_list {
        println!("{}", num);
    }
}
