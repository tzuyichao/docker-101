use std::io::stdin;

struct Visitor {
    name: String,
    greeting: String,
}

impl Visitor {
    fn new(name: &str, greeting: &str) -> Self {
        Self {
            name: name.to_lowercase(),
            greeting: greeting.to_lowercase(),
        }
    }

    fn greeting_visitor(&self) {
        println!("{}", self.greeting)
    }
}

fn what_is_your_name() -> String {
    let mut your_name = String::new();
    stdin()
        .read_line(&mut your_name)
        .expect("Failed to read line");
    your_name
        .trim()
        .to_lowercase()
}

fn main() {
    println!("Hello, what's your name?");
    let name = what_is_your_name();
    let visitor_list = [
        Visitor::new("bert", "Hello, Bert, enjoy your treehouse."),
        Visitor::new("steve", "Hi, Steve. Your milk is in the fridge."),
        Visitor::new("fred", "Wow, who invited Fred?"),
    ];
    let know_visitor = visitor_list
        .iter()
        .find(|visitor| visitor.name == name);
    
    match know_visitor {
        Some(visitor) => visitor.greeting_visitor(),
        None => println!("You are not on the visitor list. Please leave.")
    }
}
