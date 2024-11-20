from stockfish import Stockfish

paramsfish = {'Write Debug Log': 'false',
                  'Contempt': 0, 'Min Split Depth': 0, 'Threads': 2,
                  'Ponder': 'true', 'Hash': 16, 'MultiPV': 3,
                  'Skill Level': 20, 'Move Overhead': 30,
                  'Minimum Thinking Time': 20, 'Slow Mover': 80,
                  'UCI_Chess960': 'false'}

stockfish = Stockfish("C:\Program Files\stockfish-10-win\Windows\stockfish_10_x64.exe",
                      depth = 15, params = paramsfish)
