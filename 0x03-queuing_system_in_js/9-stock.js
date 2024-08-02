import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, initialAvailableQuantity: 4,
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, initialAvailableQuantity: 10,
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, initialAvailableQuantity: 2,
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5,
  },
];

const getItemById = (id) => {
  for (const product of listProducts) {
    if (product.Id === id) return (product);
  }
  return null;
};

const client = createClient();

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const GET = promisify(client.get).bind(client);

  try {
    const reserved = await GET(`item.${itemId}`);
    return reserved;
  } catch (err) {
    throw new Error(err.message);
  }
};

const app = express();
const PORT = 1245;

app.get('/list_products', (req, res) => {
  res.send(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(Number(itemId));

  if (!item) {
    res.send({ status: 'Product not found' });
    return;
  }

  const reserved = await getCurrentReservedStockById(itemId);
  item.currentQuantity = item.initialAvailableQuantity - reserved;
  res.send(item);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(Number(itemId));

  if (item === null) {
    res.send({ status: 'Product not found' });
    return;
  }

  const currentReserved = await getCurrentReservedStockById(itemId);
  if (currentReserved >= item.initialAvailableQuantity) {
    res.send({ status: 'Not enough stock available', itemId });
    return;
  }

  reserveStockById(itemId, Number(currentReserved) + 1);
  res.send({ status: 'Reservation confirmed', itemId });
});

app.listen(PORT, () => {
  console.log(`app listning on port ${PORT}...`);
});
