use kafka::producer::{Producer, Record, RequiredAcks};
use kafka::consumer::{Consumer, FetchOffset, GroupOffsetStorage};
use kafka::error::Error as KafkaError;
use std::io::{self, Write};

fn produce_messages() -> Result<(), KafkaError> {
    let mut producer = Producer::from_hosts(vec!("localhost:9093".to_owned()))
        .with_ack_timeout(std::time::Duration::from_secs(1))
        .with_required_acks(RequiredAcks::One)
        .create()?;

    for i in 0..10 {
        let message = format!("Message {}", i);
        let record = Record::from_value("test.topic", message);
        producer.send(&record)?;
        println!("Send.")
    }
    
    Ok(())
}

fn consume_messages() -> Result<(), KafkaError> {
    let mut consumer = Consumer::from_hosts(vec!("localhost:9093".to_owned()))
        .with_topic("test.topic".to_owned())
        .with_group("my_consumer_group".to_owned())
        .with_fallback_offset(FetchOffset::Earliest)
        .with_offset_storage(GroupOffsetStorage::Kafka)
        .create()?;
    
    let stdout = io::stdout();
    let mut stdout = stdout.lock();
    let mut buf = Vec::with_capacity(1024);

    loop {
        let mss = consumer.poll()?;
        if mss.is_empty() {
            println!("No messages available right now.");
            return Ok(());
        }
    
        for ms in mss.iter() {
            for m in ms.messages() {
                println!(
                    "{}:{}@{}: {:?}",
                    ms.topic(),
                    ms.partition(),
                    m.offset,
                    m.value
                );
                buf.extend_from_slice(m.value);
                buf.push(b'\n');
                stdout.write_all(&buf);
            }
            let _ = consumer.consume_messageset(ms);
        }
        consumer.commit_consumed()?;
    }
}

fn main() {
    if let Err(err) = produce_messages() {
        eprintln!("Error producing messages: {:?}", err);
        return;
    }

    if let Err(err) = consume_messages() {
        eprintln!("Error consuming messages: {:?}", err);
        return;
    }
}
