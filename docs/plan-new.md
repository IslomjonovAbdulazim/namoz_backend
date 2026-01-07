# Article System Plan

## database Models

### Article
```go
type Article struct {
    ID             uuid.UUID `json:"id"`
    Title          string    `json:"title"`
    Slug           string    `json:"slug"` // content-title-slug
    Content        string    `json:"content"` // Markdown text
    Excerpt        string    `json:"excerpt"` // Short summary/teaser for list view
    CoverImage     string    `json:"cover_image"`
    // AuthorID removed as only admins publish
    CategoryID     uuid.UUID `json:"category_id"`
    Tags           []string  `json:"tags"`
    
    // Status
    IsPublished    bool      `json:"is_published"`
    PublishedAt    time.Time `json:"published_at"`
    
    // Metrics
    ViewCount      int64     `json:"view_count"`
    Importance     float64   `json:"importance_score"` // Calculated metric
    
    CreatedAt      time.Time `json:"created_at"`
    UpdatedAt      time.Time `json:"updated_at"`
}
```

### Category
```go
type Category struct {
    ID          uuid.UUID `json:"id"`
    Name        string    `json:"name"`
    Slug        string    `json:"slug"`
    Description string    `json:"description"`
}
```

## API Endpoints

### Public Endpoints

**GET /v1/articles**
- Query Params:
  - `page`, `limit`
  - `category`: Filter by category slug
  - `sort`: `latest`, `popular` (views), `important` (calculated score)
  - `search`: Search in title/content

```json
Response:
{
  "data": [
    {
      "id": "uuid",
      "title": "Getting Started with Namoz",
      "slug": "getting-started-namoz",
      "excerpt": "A comprehensive guide...",
      "cover_image": "url",
      "published_at": "2024-01-01T10:00:00Z",
      "view_count": 1250,
      "importance_score": 85.5,
      "category": {
        "name": "Guides",
        "slug": "guides"
      }
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

**GET /v1/articles/{slug}**
- Logic: Fetch article & **increment view count** (async or sync).
```json
Response:
{
  "id": "uuid",
  "title": "Getting Started with Namoz",
  "content": "# Markdown Content\n\nThis is the detailed content...",
  "author": { "name": "Admin" },
  "related_articles": [...]
}
```

### Admin Endpoints

**POST /admin/articles**
Create a new article.
```json
Request:
{
  "title": "New Update",
  "content": "# Long markdown text...",
  "excerpt": "Short summary",
  "category_id": "uuid",
  "is_published": true,
  "tags": ["update", "news"]
}
```

**PUT /admin/articles/{id}**
Update content, status, or metadata.

**POST /admin/articles/calculate-importance**
Trigger a recalculation of importance scores for all articles.
- Logic: `score = (log(view_count) * 10) + (1 / days_since_published * 100)`
- Can be run periodically via cron or manually triggered.

**POST /admin/articles/upload/image**
Upload article images (cover or content).
- Max size: 500KB
- Allowed types: JPEG, PNG, WEBP
```json
Response:
{
  "url": "https://storage.googleapis.com/..."
}
```

**GET /admin/articles/stats**
Get analytics about article performance.
```json
{
  "total_views": 50000,
  "most_read_article": { ... },
  "articles_published_this_month": 5
}
```
