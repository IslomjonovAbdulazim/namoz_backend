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

**GET /v1/articles** (Implemented)
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

**GET /v1/articles/{slug}** (Implemented)
- Logic: Fetch article & **increment view count** (async or sync).
> [!NOTE]
> `author` and `related_articles` fields are currently missing in the implementation.
```json
Response:
{
  "id": "uuid",
  "title": "Getting Started with Namoz",
  "content": "# Markdown Content\n\nThis is the detailed content...",
  // "author": { "name": "Admin" }, // Missing in code
  // "related_articles": [...] // Missing in code
}
```

### Admin Endpoints

> [!IMPORTANT]
> All admin endpoints require `Authorization: Bearer <token>` header.

**POST /admin/categories**
Create a new category.
```json
Request:
{
  "name": "Guides",          // Required, 1-100 chars
  "slug": "guides",          // Required, 1-100 chars, Unique
  "description": "Tutorials" // Optional
}

Response (200 OK):
{
  "name": "Guides",
  "slug": "guides",
  "description": "Tutorials",
  "id": "uuid-string"
}
```

**PUT /admin/categories/{id}**
Update category.
```json
Request:
{
  "name": "Updated Name",
  "slug": "updated-slug"
}
```

**DELETE /admin/categories/{id}**
Delete category (only if it has no articles).

**POST /admin/articles**
Create a new article.
```json
Request:
{
  "title": "New Update",              // Required, 1-255 chars
  "slug": "new-update-2024",          // Required, 1-255 chars, Unique
  "content": "# Markdown Content...", // Required, string
  "category_id": "uuid-string",       // Required, valid Category UUID
  
  // Optional Fields
  "excerpt": "Short summary",         // Optional, used for previews
  "cover_image": "https://...",       // Optional URL (from upload endpoint)
  "is_published": true,               // Optional, default: false
  "tags": ["update", "news"]          // Optional array of strings, default: []
}

Response (200 OK):
{
  "id": "uuid-string",
  "title": "New Update",
  "slug": "new-update-2024",
  "content": "# Markdown Content...",
  "excerpt": "Short summary",
  "cover_image": "https://...",
  "category_id": "uuid-string",
  "tags": ["update", "news"],
  "is_published": true,
  "published_at": "2024-01-07T12:00:00Z",
  "view_count": 0,
  "importance_score": 0,
  "created_at": "2024-01-07T12:00:00Z",
  "updated_at": "2024-01-07T12:00:00Z",
  "category": null
}
```

**GET /admin/articles/{id}**
Get a single article by ID for editing.

**PUT /admin/articles/{id}**
Update article. Send only fields you want to change.
```json
Request:
{
  "title": "Updated Title",
  "is_published": false
}
```

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
