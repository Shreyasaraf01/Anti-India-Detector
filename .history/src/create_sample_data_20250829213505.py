import pandas as pd
rows = [
  ("I think the government's actions are hurting our nation", 1),
  ("This article spreads false claims about India", 1),
  ("Support local businesses and our people", 0),
  ("New policy is bad for farmers, it's worrying", 1),
  ("I love visiting India, beautiful places", 0),
  ("That news story about our army is fake", 1),
  ("Check out these travel photos from India", 0),
  ("This post tries to make people hate India with lies", 1),
  ("Study tips for students", 0),
  ("False rumours about citizens are being shared", 1)
]
df = pd.DataFrame(rows, columns=['text','label'])
df.to_csv("data/sample_data.csv", index=False)
print("Created data/sample_data.csv with", len(df), "rows")
