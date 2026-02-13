---
title: Automated Embedding Generation
impact: MEDIUM
impactDescription: Server-side embedding can eliminate client-side pipelines
tags: automated-embedding, autoEmbed, vectorSearch, voyage, atlas
---

## Automated Embedding Generation

MongoDB Atlas supports automated embedding generation, eliminating the need for client-side embedding pipelines. Atlas handles embedding creation server-side using managed models.

Using incorrect syntax or outdated model references causes index creation failures.

**Incorrect (using wrong field type for automated embedding):**

```javascript
// WRONG - using "text" type instead of "autoEmbed"
db.listingsAndReviews.createSearchIndex("vector_index", "vectorSearch", {
  fields: [{
    type: "text",
    path: "summary",
    model: "voyage-3-large"
  }]
})
```

**Correct (Atlas automated embedding with `autoEmbed`):**

```javascript
// Index definition with automated embedding
db.listingsAndReviews.createSearchIndex("vector_index", "vectorSearch", {
  fields: [
    {
      type: "autoEmbed",
      modality: "text",
      path: "summary",
      model: "voyage-4"
    },
    { type: "filter", path: "address.country" },
    { type: "filter", path: "bedrooms" }
  ]
})

// Query with text input (Atlas generates query embedding)
db.listingsAndReviews.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "summary",
      filter: {
        bedrooms: { $gte: 3 },
        "address.country": { $in: ["United States"] }
      },
      query: { text: "close to amusement parks" },
      model: "voyage-4",
      numCandidates: 100,
      limit: 10
    }
  }
])
```

**Supported Models (`autoEmbed`):**

| Model | Dimensions | Best For |
|-------|------------|----------|
| `voyage-4-lite` | provider-defined | High-volume, cost-sensitive workloads |
| `voyage-4` | provider-defined | General semantic search (recommended baseline) |
| `voyage-4-large` | provider-defined | Maximum semantic accuracy |
| `voyage-code-3` | provider-defined | Code and technical-document retrieval |

**Requirements:**

- M10+ Atlas cluster
- Voyage API key(s) configured for indexing/query
- Preview feature: validate behavior and check Atlas documentation for current enrollment status

**When Automated Embedding is Triggered:**

```javascript
// 1. On document INSERT - embedding auto-generated
await db.products.insertOne({
  content: "New product description"
})

// 2. On document UPDATE - embedding auto-regenerated
await db.products.updateOne(
  { _id: productId },
  { $set: { content: "Updated product description" } }
)

// 3. On bulk INSERT/UPDATE - batch embedding
await db.products.insertMany(documents)
```

**Combining Automated Embedding with Pre-Filtering:**

```javascript
db.listingsAndReviews.createSearchIndex("vector_index", "vectorSearch", {
  fields: [
    {
      type: "autoEmbed",
      modality: "text",
      path: "summary",
      model: "voyage-4"
    },
    {
      type: "filter",
      path: "address.country"
    }
  ]
})

db.listingsAndReviews.aggregate([
  {
    $vectorSearch: {
      index: "vector_index",
      path: "summary",
      query: { text: "family-friendly home near parks" },
      model: "voyage-4",
      filter: { "address.country": "United States" },
      numCandidates: 100,
      limit: 10
    }
  }
])
```

**Manual vs Automated Comparison:**

| Aspect | Manual Embedding | Automated Embedding |
|--------|-----------------|---------------------|
| Client code | Required | Not needed |
| Model flexibility | Any model you integrate | Managed Voyage-model set |
| Cost control | Client-side | Server-side billing |
| Query input | Precomputed vectors | Natural-language text query support |
| Availability | GA patterns | Preview — check Atlas docs for status |

**When NOT to use this pattern:**

- You need full control over embedding provider/model lifecycle
- You must reuse raw embedding vectors outside MongoDB workflows
- Your compliance or platform constraints don't match preview requirements

## Verify with

1. Run the "Correct" index or query example on a staging dataset.
2. Validate expected behavior and performance using explain and Atlas metrics.
3. Confirm feature availability on your Atlas cluster tier before production rollout.

Reference: [MongoDB Auto-Generated Embeddings](https://mongodb.com/docs/atlas/atlas-vector-search/crud-embeddings/create-embeddings-automatic/)
