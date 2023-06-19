use std::time::Duration;
use zookeeper::Watcher;
use zookeeper::WatchedEvent;
use zookeeper::ZooKeeper;

struct NoopWatcher;

impl Watcher for NoopWatcher {
    fn handle(&self, _ev: WatchedEvent) {}
}

fn main() {
    let zk = ZooKeeper::connect("Server:2181", Duration::from_millis(2500), NoopWatcher).unwrap();
    let broker_ids = zk.get_children("/brokers/ids", false);
    match broker_ids {
        Ok(children) => {
            println!("/brockers/ids children: {:?}", children);
            if !children.is_empty() {
                let node_path = format!("/brokers/ids/{}", children[0]);
                let broker = zk.get_data(&node_path, false);
                match broker {
                    Ok((data, stat)) => {
                        println!("Broker: {:?}", data);
                        println!("Stat: {:?}", stat);
                        println!("Data: {:?}", String::from_utf8_lossy(&data).to_string());
                    }
                    Err(err) => {
                        println!("Failed to get {} data: {:?}", node_path, err);
                    }
                }
            }
        }
        Err(err) => {
            println!("Failed to get /brokers/ids children: {:?}", err);
        }
    }

    std::thread::sleep(std::time::Duration::from_secs(10));
}