export interface Product {
  id: number | string;
  name: string;
  price: number;
  image: string;
  description?: string;
  originalPrice?: number;
  discount?: string;
  rating?: number;
  reviewCount?: number;
}
