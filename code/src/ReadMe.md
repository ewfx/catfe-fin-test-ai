I'll add the OpenAI API key instructions to the README:

```markdown:README.md
# AI Test Case Generator

## 🔑 Getting Your OpenAI API Key

### Step 1: Create OpenAI Account
1. Visit [OpenAI's website](https://platform.openai.com/signup)
2. Click "Sign Up"
3. Choose your registration method (email or Google/Microsoft account)
4. Complete the verification process

### Step 2: Access API Keys
1. Log in to [OpenAI Platform](https://platform.openai.com)
2. Click on your profile icon in the top-right corner
3. Select "View API keys"
4. Click "Create new secret key"
5. Give your key a name (optional)
6. Copy your API key immediately (it won't be shown again!)

### Step 3: Set Up API Key in Project
1. Create a `.env` file in your project root:
   ```bash
   # For Windows
   copy .env.example .env

   # For macOS/Linux
   cp .env.example .env
   ```

2. Add your API key to `.env`:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

### ⚠️ Important Security Notes
- Never commit your API key to version control
- Keep your `.env` file in `.gitignore`
- Don't share your API key with others
- Regenerate your key if it's ever exposed

## 🔄 Switching to Free Tier Models

### 1. Update Your `.env` File
Change your model settings in the `.env` file:

```env
# For paid tier (default)
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000

# For free/lower-cost tier (recommended for starting)
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2048
```

### 2. Model Options Explained

#### GPT-4 (Paid Tier)
- Model: `gpt-4`
- Max Tokens: 8192
- Best quality but more expensive
- Better for complex test case generation

#### GPT-3.5-Turbo (Free/Lower-cost Tier)
- Model: `gpt-3.5-turbo`
- Max Tokens: 4096
- Good balance of quality and cost
- Suitable for most test case generation

#### GPT-3.5-Turbo 16K (Alternative)
- Model: `gpt-3.5-turbo-16k`
- Max Tokens: 16384
- Good for larger requirements documents
- Still cheaper than GPT-4

### 3. Token Limit Guidelines
- Set `OPENAI_MAX_TOKENS` to about half of the model's maximum context length
- For GPT-3.5-Turbo: use 2048 tokens
- For GPT-3.5-Turbo-16K: can use up to 8192 tokens
- Larger values might result in API errors

### 4. Cost Considerations
- GPT-3.5-Turbo is approximately 10x cheaper than GPT-4
- Good for initial development and testing
- Can upgrade to GPT-4 for production or complex cases

### 5. Performance Expectations
When using GPT-3.5-Turbo, expect:
- Slightly less comprehensive test cases
- May need more prompt refinement
- Still suitable for most testing scenarios
- Faster response times

### 6. Best Practices
- Start with GPT-3.5-Turbo for development
- Test your requirements with smaller token limits first
- Monitor API usage and costs
- Gradually increase tokens if needed

### 7. Managing API Costs
- Monitor usage in [OpenAI Dashboard](https://platform.openai.com/usage)
- Set up billing limits in [OpenAI Billing](https://platform.openai.com/account/billing/limits)
- New accounts get some free credits to start
- Consider setting up usage alerts

Need help? Check [OpenAI's Documentation](https://platform.openai.com/docs/introduction) or raise an issue in this repository.
```

Would you like me to add any other sections or clarify anything in these instructions?
