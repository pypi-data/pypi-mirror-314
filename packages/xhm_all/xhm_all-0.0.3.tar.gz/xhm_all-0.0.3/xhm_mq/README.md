### mq sdk

#### 快速搭建一个mq

    docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

### 生产者Demo

    import json
    
    from xhm_mq.rabbitmq_producer import RabbitmqProducer
    
    producer = RabbitmqProducer(host="10.1.251.235", port=5672, exchange='soulpal', routing_key='wechat_send_queue')
    
    if __name__ == '__main__':
        producer.publish(json.dumps({"type": "text", "msg": "hello world"}, ensure_ascii=False))

### 消费者Demo

    from xhm_mq.rabbitmq_consumer import RabbitmqConsumer
    
    consumer = RabbitmqConsumer(host="10.1.251.235", port=5672, exchange='soulpal', routing_key='wechat_send_queue')
    
    if __name__ == "__main__":
        def on_message_received(channel, method_frame, header_frame, body):
            print(f"Received message: {body.decode()}")
    
    
        consumer.consume(on_message_received)
