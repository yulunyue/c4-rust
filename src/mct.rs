mod mcts {

    macro_rules! parse_input {
        ( $ x : expr , $ t : ident ) => {
            $x.trim().parse::<$t>().unwrap()
        };
    }
    pub struct MCTS {
        pool: Pool,
        root: Box<Node>,
        nn: NNManager,
        r: ThreadRng,
    }
    impl Drop for MCTS {
        fn drop(&mut self) {
            let mut new_r = Box::new(Node::new());
            swap(&mut new_r, &mut self.root);
            self.pool.push(new_r);
            self.pool.ptrs.drain(..).for_each(|n| {
                Box::into_raw(n);
            });
        }
    }
    impl MCTS {
        pub fn new() -> MCTS {
            let mut mcts = MCTS {
                pool: Pool::new(2000000),
                root: Box::new(Node::new()),
                nn: NNManager {
                    cache: HashMap::new(),
                    nn: NN::new(),
                    access: 0,
                    hit: 0,
                },
                r: rand::thread_rng(),
            };
            mcts.nn.nn.read_weights();
            for _ in 0..2 {
                mcts.root.playout(&mut mcts.nn, &mut mcts.pool);
            }
            mcts
        }
        pub fn clear(&mut self) {
            let mut a = self.pool.pop();
            swap(&mut a, &mut self.root);
            self.pool.push(a);
        }
        fn update_with_action(&mut self, action: u8) {
            if self.root.children.is_empty() {
                self.root.select(&mut self.nn, &mut self.pool);
            }
            let mut new_root = Option::None;
            while self.root.children.len() > 0 {
                if self.root.children.last().unwrap().game.last_move == action {
                    new_root = Some(self.root.children.pop().unwrap());
                } else {
                    self.pool.push(self.root.children.pop().unwrap());
                }
            }
            mem::swap(new_root.as_mut().unwrap(), &mut self.root);
            self.pool.push(new_root.unwrap());
        }

        fn get_move_probs_play(&mut self, endt: Instant) -> u8 {
            while Instant::now() < endt {
                self.root.playout(&mut self.nn, &mut self.pool);
            }
            let a = self.root.children.iter().max_by_key(|b| {
                if self.root.terminal {
                    b.value as i32
                } else {
                    b.visits
                }
            });
            eprintln!("root visits: {}", self.root.visits);
            a.unwrap().game.last_move
        }

        pub fn cg(&mut self) {
            let mut endt;
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).unwrap();
            let mut my_last: i32 = -1;
            for i in 0..65 {
                io::stdin().read_line(&mut input_line).unwrap();
                for _ in 0..7 as usize {
                    io::stdin().read_line(&mut input_line).unwrap();
                }
                input_line.clear();
                io::stdin().read_line(&mut input_line).unwrap();
                let num_valid_actions = parse_input!(input_line, i32);
                for _ in 0..num_valid_actions as usize {
                    io::stdin().read_line(&mut input_line).unwrap();
                }
                input_line.clear();
                io::stdin().read_line(&mut input_line).unwrap();
                if i == 0 {
                    endt = Instant::now() + Duration::from_millis(900);
                } else {
                    endt = Instant::now() + Duration::from_millis(100);
                }
                if my_last != -1 {
                    self.update_with_action(my_last as u8);
                }
                let mut hard_coded: i32 = -1;
                if input_line != "STEAL" {
                    let opp_action = parse_input!(input_line, i32);
                    if opp_action >= 0 {
                        self.update_with_action(opp_action as u8);
                    }
                    if opp_action == -1 {
                        hard_coded = 1;
                        self.update_with_action(hard_coded as u8);
                        my_last = -1;
                    } else if i == 0 {
                        hard_coded = -2;
                    }
                }
            }
        }
    }
}
