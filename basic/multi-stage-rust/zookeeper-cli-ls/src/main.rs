use std::env;
use std::process;
use std::time::Duration;

use zookeeper::{WatchedEvent, Watcher, ZooKeeper};

struct MyWatcher;

impl Watcher for MyWatcher {
    fn handle(&self, _: WatchedEvent) {}
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Provider zookeeper and command");
        process::exit(1);
    }

    let server_list = &args[1];
    let servers: Vec<&str> = server_list.split(',').collect();

    let zk = ZooKeeper::connect(&servers.join(","), Duration::from_secs(5), MyWatcher).unwrap();

    let list_command = |path: &str| {
        match zk.get_children(path, false) {
            Ok(children) => {
                println!("Directory {} content: ", path);
                for child in children {
                    println!("{}", child);
                }
            }
            Err(err) => {
                eprintln!("Cannot get directory {} content: {}", path, err);
            }
        }
    };

    let get_command = |path: &str| {
        match zk.get_data(path, false) {
            Ok(data) => {
                println!("Document {} Content: \n{:?}", path, data);
            }
            Err(err) => {
                eprintln!("Can not read {} content: {}", path, err);
            }
        }
    };

    let command = &args[2];
    let path = &args[3];

    match command.as_str() {
        "ls" => list_command(path),
        "get" => get_command(path),
        _ => {
            eprintln!("command not found");
            process::exit(1);
        }
    }
}
